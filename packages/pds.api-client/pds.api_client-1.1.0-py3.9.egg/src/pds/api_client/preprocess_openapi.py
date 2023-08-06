import json


def main():
    with open('swagger.json', 'r') as fi:
        openapi = json.load(fi)
        for key, response in openapi['components']['responses'].items():
            if '*' in response['content']:
                print(f"remove * content for {key}")
                response['content'].pop('*')

    with open('preprocessed-swagger.json', 'w') as fo:
        json.dump(openapi, fo)
            
if __name__ == '__main__':
    main()