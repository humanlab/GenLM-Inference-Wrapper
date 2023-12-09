import argparse
import math
from tqdm import tqdm

from genlm_inference import GenLMInferenceWrapper, PromptTemplater
from genlm_inference.constants import BATCH_SIZE, SOCIALITE_CHECKPOINT
from data_connector.dcConstants import MAX_SQL_SELECT, BATCH_SIZE
from data_connector.database.query import QueryBuilder, Column
from data_connector.database.dataEngine import DataEngine


def parse_args():
    args = argparse.ArgumentParser()
    args.add_argument("--database", "-d", type=str, help="Database name", required=True)
    args.add_argument("--table", "-t", type=str, help="Message Table name", required=True)
    args.add_argument("--messageid_field", type=str, default="message_id", help="Message ID field name")
    args.add_argument("--message_field", type=str, default="message", help="Message field name")
    args.add_argument("--instruction", "-i", type=str, help="Instruction for the task", required=True)
    args.add_argument("--output_table", type=str, \
                    help="Output table name. DLATK convention: feat$<feature_name>$<table_name>$<group_field>. Ensure the feature name reflects the name of the model and the instruction")
    args.add_argument("--model_path", type=str, default=SOCIALITE_CHECKPOINT, help="Path to the model checkpoint")
    args.add_argument("--mysql_config_file", type=str, default="~/.my.cnf", help="MySQL config file")
    args.add_argument("--batch_size", type=int, default=BATCH_SIZE, help="Batch size for inference")
    # args.add_argument("--cache_dir", type=str, default="~/.cache/socialite/v1", help="Cache directory for socialite")
    return args.parse_args()


def get_messages(args: argparse.Namespace, qb: QueryBuilder):
    num_messages = qb.create_select_query(from_table=args.table).set_fields(["COUNT(1)"]).where('{} IS NOT NULL AND LENGTH({}) > 0'.format(args.message_field, args.message_field)).execute_query()[0][0]
    query = qb.create_select_query(from_table=args.table).set_fields([args.messageid_field, args.message_field]).where('{} IS NOT NULL AND LENGTH({}) > 0'.format(args.message_field, args.message_field))
    cursor = query.execute_query(get_cursor=True)
    return cursor, num_messages
    

def create_output_table(args: argparse.Namespace, qb: QueryBuilder):
    
    # Step 1: Retrieve the datatype of message_id_field from args.table 
    message_id_type_query = qb.create_select_query(from_table="INFORMATION_SCHEMA.COLUMNS").set_fields(["DATA_TYPE"]).where("TABLE_NAME = '{}' AND COLUMN_NAME = '{}'".format(args.table, args.messageid_field))
    message_id_type = message_id_type_query.execute_query()[0][0]
    
    # Step 2: Create a new table "output_table" with message_id_field as primary key, message_field, instruction and output
    message_id_col = Column(column_name=args.messageid_field, datatype=message_id_type, primary_key=True, unsigned="UNSIGNED" in message_id_type)
    message_col = Column(column_name=args.message_field, datatype="text")
    instruction_col = Column(column_name="instruction", datatype="text")
    output_col = Column(column_name="output", datatype="text")
    create_table_query = qb.create_createTable_query(table=args.output_table).add_columns(cols=[message_id_col, message_col, instruction_col, output_col])
    create_table_query.execute_query()
    
    return args.output_table


def write_to_table(data: list, args: argparse.Namespace, qb: QueryBuilder):
        
    # Step 1: Create a qb for insert query
    values = [(args.messageid_field, ""), (args.message_field, ""), ("instruction", ""), ("output", "")]
    insert_query = qb.create_insert_query(into_table=args.output_table).set_values(values=values)
    
    # Step 2: Insert data into the output_table
    insert_query.execute_query(insert_rows=data)
    

if __name__ == '__main__':
    args = parse_args()

    data_engine = DataEngine(corpdb=args.database, mysql_config_file=args.mysql_config_file)
    data_engine.connect()
    qb = QueryBuilder(data_engine)
    cursor, num_messages = get_messages(args=args, qb=qb)
    
    print ("-----------------------")
    print ("Total number of messages: {}".format(num_messages))
    print ("-----------------------")

    templater = PromptTemplater()
    model = GenLMInferenceWrapper(model_checkpoint=args.model_path)
    
    table_name = create_output_table(args=args, qb=qb)
    
    print ("-----------------------")
    print ("Output table created: {}".format(table_name))
    print ("-----------------------")

    five_percent = math.ceil(num_messages * 0.05)
    num_global_iters = math.ceil(num_messages / float(MAX_SQL_SELECT))
    message_idx = 0
    progress_bar = tqdm(total=num_messages)
    for global_iter in range(num_global_iters):
        response = cursor.fetchmany(size=MAX_SQL_SELECT)
        num_batches = math.ceil(len(response) / float(args.batch_size))
        # print (f"Number of batches, len response: {num_batches}/{len(response)}")
        
        for batch_idx in range(num_batches):
            id = [r[0] for r in response][batch_idx*args.batch_size:(batch_idx+1)*args.batch_size]
            input_data = [r[1] for r in response][batch_idx*args.batch_size:(batch_idx+1)*args.batch_size]
            input_prompt = templater(input_text=input_data, instruction=args.instruction)

            prediction_data = model.generate_outputs(input_data=input_prompt)
            prediction_data = [(id[jdx], input_data[jdx], datadict['text'], datadict['generated_text']) for jdx, datadict in enumerate(prediction_data)]

            write_to_table(data=prediction_data, args=args, qb=qb)
            progress_bar.update(args.batch_size)
            message_idx += args.batch_size
            # batch_idx += 1
            
            # if message_idx % five_percent == 0:
            #     print ("-----------------------")
            #     print ("{}% of messages processed".format(message_idx*100/num_messages))
            #     print ("-----------------------")

        progress_bar.close()
    print ("-----------------------")
    print ("Successfully Finised Running the Inference ¯\_(ツ)_/¯")
    print ("-----------------------")