import json
import urllib.parse
import boto3

print('Loading function')

client = boto3.client('lambda')
#layerName='gu2-test-delete'
#versionsToKeep = 'event['VersionsToKeep']'

def lambda_handler(event, context):
    version_list = client.list_layer_versions(
        LayerName= event['layerName']
    )['LayerVersions']
    

    if len(version_list) <= event['VersionsToKeep']:
        print('last', event['VersionsToKeep'], 'layer versions cannot be deleted')
        exit()
        
    toBeDeleted = version_list[event['VersionsToKeep']:]
    for i in toBeDeleted:
        deleteVersion= i['Version']
        client.delete_layer_version(
            LayerName= event['layerName'],
            VersionNumber= deleteVersion
        )
        print('Deleted layer version',deleteVersion) 
            

