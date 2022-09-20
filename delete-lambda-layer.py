import json
import urllib.parse
import boto3

print('Loading function')

client = boto3.client('lambda')


def lambda_handler(event, context):
    version_list = client.list_layer_versions(
        LayerName= event['layerName']
    )['LayerVersions']
    

    if len(version_list) <= event['VersionsToKeep']:
        print('last', event['VersionsToKeep'], 'layer versions cannot be deleted')
        return {
            "statusCode": 200,
            "message": ('last ' + str(event['VersionsToKeep']) + ' layer versions cannot be deleted')
        }
        
    print("Trying to delete lambda laters for -",event['layerName'])
    
    toBeDeleted = version_list[event['VersionsToKeep']:]
    for i in toBeDeleted:
        deleteVersion= i['Version']
        try:
            client.delete_layer_version(
                LayerName= event['layerName'],
                VersionNumber= deleteVersion
            )
            print('Deleted layer version',deleteVersion)
        except Exception as e:
            print(e)
            raise Exception(e)
    
    print('previous', len(toBeDeleted), 'Layer/s deleted successfully')        
    return {
        "message": ('Previous ' + str(len(toBeDeleted)) + ' Layer/s deleted successfully')
    }
