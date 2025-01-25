import os
import sys
from pathlib import Path
from typing import Tuple
from dotenv import load_dotenv
import docker
from autogen import AssistantAgent, UserProxyAgent
from autogen.coding import DockerCommandLineCodeExecutor

# Constants
DOCKER_IMAGE = "python:3.9-slim"
DOCKER_TIMEOUT = 60
MODEL_NAME = "llama3-70b-8192"

class AgentSetup:
    @staticmethod
    def setup_directories() -> Tuple[Path, Path]:
        """Create and return work and output directories"""
        base_dir = Path(__file__).parent
        work_dir = base_dir / "output/agent"
        output_dir = base_dir / "output" / "agent"  # Fixed: directly create output_dir path
        
        work_dir.mkdir(exist_ok=True, parents=True)
        output_dir.mkdir(exist_ok=True, parents=True)
        
        return work_dir, output_dir

    @staticmethod
    def setup_docker() -> bool:
        """Initialize Docker environment"""
        try:
            client = docker.from_env()
            client.ping()
            
            try:
                client.images.pull(DOCKER_IMAGE)
            except docker.errors.ImageNotFound:
                client.images.get(DOCKER_IMAGE)
                print("Using existing local image")
            
            return True
        except Exception as e:
            print(f"Docker setup failed: {str(e)}")
            return False

class AgentFactory:
    @staticmethod
    def create_system_message() -> str:
        return """You are a helpful AI assistant that executes code in a Docker container.
        Only ask for user input when:
        1. You need an API key or credentials
        2. You have completed a task and need new instructions
        3. You need crucial information that cannot be inferred
        Always explain what you're doing before asking for input.
        Save all outputs to the /workspace/output directory."""

    @staticmethod
    def create_agents(work_dir: Path, output_dir: Path) -> Tuple[AssistantAgent, UserProxyAgent, DockerCommandLineCodeExecutor]:
        """Create and configure all necessary agents"""
        # Configure LLM
        config_list = [{
            "model": MODEL_NAME,
            "api_key": os.getenv("api_key"),
            "api_type": "groq"
        }]

        # Setup Docker executor
        executor = DockerCommandLineCodeExecutor(
            timeout=DOCKER_TIMEOUT,
            work_dir=str(work_dir),
            image=DOCKER_IMAGE
        )
        
        # Link output directory
        output_link = work_dir / "output"
        if not output_link.exists():
            output_link.symlink_to(output_dir)
        
        # Create agents
        assistant = AssistantAgent(
            name="assistant",
            system_message=AgentFactory.create_system_message(),
            llm_config={"config_list": config_list}
        )
        
        user_proxy = UserProxyAgent(
            name="user_proxy",
            code_execution_config={"executor": executor},
            human_input_mode="ALWAYS"
        )
        
        return assistant, user_proxy, executor

def main():
    """Main execution flow"""
    # Initialize
    load_dotenv()
    work_dir, output_dir = AgentSetup.setup_directories()
    
    # Verify Docker
    if not AgentSetup.setup_docker():
        sys.exit(1)

    try:
        # Create and run agents
        assistant, user_proxy, executor = AgentFactory.create_agents(work_dir, output_dir)
        with executor:
            print("AI Assistant initialized. Starting conversation...")
            user_proxy.initiate_chat(
                assistant,
                message="Hello! I'm ready to help you with tasks. What would you like me to do?"
            )
    except Exception as e:
        print(f"Error during execution: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()