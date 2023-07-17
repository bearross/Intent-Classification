import os
import openai
from dotenv import load_dotenv, find_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.output_parsers import ResponseSchema, StructuredOutputParser

class RealEstateAssistant:
    def __init__(self):
        load_dotenv(find_dotenv())
        openai.api_key = os.getenv('OPENAI_API_KEY')

        self.possible_intents = [
            "CreateObject",
            "List",
            "Report",
            "ReviewObject",
            "Workflow"
        ]

        self.possible_objects = [
            "Bank account",
            "Bank reconciliation",
            "Contact",
            "Customer",
            "Entry",
            "Journal",
            "Maintenance",
            "Owner",
            "Payable",
            "Property",
            "Prospect",
            "Accounts Receivable",
            "Tenant",
            "Units",
            "Vendor",
        ]

        self.output_parser = self.create_output_parser()
        self.format_instructions = self.output_parser.get_format_instructions()
        self.chat_prompt = self.create_chat_prompt()

        self.chat = ChatOpenAI(temperature=0.0)


    def create_output_parser(self) -> StructuredOutputParser:
        first_order_intent_schema = ResponseSchema(
            name="FirstOrderIntent",
            description="The firstOrder intent of the real-state statement"
        )
        second_order_intent_schema = ResponseSchema(
            name="SecondOrderIntent",
            description="The secondOrder intent of the real-state statement"
        )

        entities_schema = ResponseSchema(
            name="Entities",
            description="List of all entities in the real-estate statement. Separate each entity by comma."
        )
        response_schemas = [first_order_intent_schema, second_order_intent_schema, entities_schema]

        return StructuredOutputParser.from_response_schemas(response_schemas)


    def create_chat_prompt(self) -> ChatPromptTemplate:
        template_filename = "prompt.txt"
        with open(template_filename, "r") as template_file:
            template_string = template_file.read()

        system_message_prompt = SystemMessagePromptTemplate.from_template(template_string)
        human_template = "statement: ```{statement}```"
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

        return ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])


    def classify(self, statement: str) -> dict:
        messages = self.chat_prompt.format_prompt(
            possible_intents=self.possible_intents,
            possible_objects=self.possible_objects,
            format_instructions=self.format_instructions,
            statement=statement
        ).to_messages()
        response = self.chat(messages)
        return self.output_parser.parse(response.content)

if __name__ == '__main__':
    assistant = RealEstateAssistant()
    statement = input("Enter your statement: ")
    print(assistant.classify(statement))
