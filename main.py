from app import create_app, start_dev_server
from ai_comm_system import setup as setup_comms

web_app = create_app(attach=[setup_comms])

if __name__ == '__main__':
    start_dev_server(web_app)
