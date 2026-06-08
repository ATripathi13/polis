"""
Polis AI Agents — Base Agent Class
"""

from typing import Any, Type, TypeVar
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from app.config import settings

T = TypeVar("T", bound=BaseModel)


class BaseAgent:
    """
    Base class for all Polis specialized agents.
    Provides LLM initialization and structured output parsing.
    """

    def __init__(self, system_prompt: str, output_schema: Type[T] = None):
        self.llm = ChatOpenAI(
            model=settings.openai_model,
            api_key=settings.openai_api_key,
            temperature=0, # Deterministic output for operational intelligence
        )
        self.system_prompt = system_prompt
        self.output_schema = output_schema
        self.parser = PydanticOutputParser(pydantic_object=output_schema) if output_schema else None

    def get_prompt_template(self) -> ChatPromptTemplate:
        """Create a prompt template with system and human roles."""
        messages = [("system", self.system_prompt)]
        
        if self.parser:
            messages.append(
                ("system", "\n\nCRITICAL: The output MUST be a valid JSON matching the following schema:\n{format_instructions}")
            )
            
        messages.append(("human", "{input_text}"))
        return ChatPromptTemplate.from_messages(messages)

    async def run(self, input_text: str, **kwargs) -> Any:
        """Execute the agent on the given input."""
        prompt_values = {"input_text": input_text, **kwargs}
        if self.parser:
            prompt_values["format_instructions"] = self.parser.get_format_instructions()
        
        prompt = self.get_prompt_template()
        chain = prompt | self.llm
        
        response = await chain.ainvoke(prompt_values)
        
        if self.parser:
            return self.parser.parse(response.content)
        
        return response.content
