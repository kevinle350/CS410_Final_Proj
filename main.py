import bedrock
import webpage

if __name__ == '__main__':
    bedrock.setup()
    webpage.app.run_server(debug=True)