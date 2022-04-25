import awsgi
import main
from main import app

def lambda_handler(event, context):
    return awsgi.response(app, event, context, base64_content_types={"image/png"})


def main():
    print("Hello World!")

if __name__ == "__main__":
    main()
