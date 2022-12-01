import boto3
import json

def get_ec2_instance_hourly_price():
              
    client = boto3.client('ec2')
    
    response = client.describe_instances()
    ec2_resource = boto3.resource('ec2')
    
    #print(instance) 

    
    #all_ec2_instances = response['Instances']

    for r in response['Reservations']:
        for i in r['Instances']:

            print(i['InstanceId'])
            print(i['InstanceType'])
            print(i['PlatformDetails'])

            instanceId = i['InstanceId']
            instanceType = i['InstanceType']
            instancePlatform = i['PlatformDetails']
#            ec2_offer = awspricing.offer('AmazonEC2')
            instancePrice = price_information(instanceType, 'Linux')
#            instancePrice = ec2_offer.ondemand_hourly(instanceType, operating_system ='Linux', region='eu-central-1')
            print(instancePrice)

    return 1


def price_information(instance_type, os):
        # Search product filter
        FLT = '[{{"Field": "operatingSystem", "Value": "{o}", "Type": "TERM_MATCH"}},' \
              '{{"Field": "instanceType", "Value": "{t}", "Type": "TERM_MATCH"}}]'
        pricing = boto3.client('pricing', region_name='us-east-1')
        i = 0
        f = FLT.format(t=instance_type, o=os)
        try:
            data = pricing.get_products(ServiceCode='AmazonEC2', Filters=json.loads(f))
            instance_price = 0
            for price in data['PriceList']:
                try:
                    first_id =  list(eval(price)['terms']['OnDemand'].keys())[0]
                    price_data = eval(price)['terms']['OnDemand'][first_id]
                    second_id = list(price_data['priceDimensions'].keys())[0]
                    instance_price = price_data['priceDimensions'][second_id]['pricePerUnit']['USD']
                    print(instance_price)
                    
                    print(price_data['priceDimensions']) ##

                    if float(price) > 0:
                        break
                except Exception as e:
                    i = i + 1
            return instance_price
        except Exception as e:
#            print(e)
            return 0

ec2_instance_price = get_ec2_instance_hourly_price()
print(ec2_instance_price)