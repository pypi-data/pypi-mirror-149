from datetime import datetime,timedelta
import boto3

def latest_files(s3client, bucket, prefix="", suffix="",last_modified_date=None):

    """
    Generate details of the objects in an S3 bucket based on last_modified_date.

    Args:
        s3client:
            boto3 S3 client
        bucket:
            Name of the S3 bucket.
        prefix:
            Only fetch objects whose key starts with this prefix (optional).
        suffix:
            Only fetch objects whose keys end with this suffix (optional).
        last_modified_date: Only yield objects with LastModified dates greater or equal to this value (optional).

    Returns:
        Dictionary objects for each qualifying S3 object through a generator. The dict includes:
            key
                the object key (name)
            size
                the size of the object in bytes (integer)
            last_modified
                the datetime object of which has modified based on parameter last_modified_date or by defualt 1 day before current date
    """
    # Setup time delta for s3 objects returns at yesterday date always 
    if last_modified_date is None:
        last_modified_date =(datetime.now() - timedelta(1)).strftime('%Y-%m-%d')
    else:
        last_modified_date=last_modified_date
    
    # Use a paginator to allow for large list sizes.
    paginator = s3client.get_paginator("list_objects_v2")

    # s3 list objects treats a leading slash as a folder named "/"
    if prefix.startswith("/"):
        prefix = prefix[1:]

    # Define parameters for the S3 call. The prefix filter is applied where.
    list_parameters = {"Bucket": bucket, "Prefix": prefix}
    # The paginator will return the results in a series of pages (default is 1000 objects per page)
    qualifying_objects = []
    for page in paginator.paginate(**list_parameters):
        if page["KeyCount"] > 0:
            # Loop each page
            for content in page["Contents"]:                                
                obj_last_modified=content["LastModified"].date().strftime('%Y-%m-%d')
                # Loop through each S3 object on the page.
                if content["Key"].endswith(suffix) and obj_last_modified >=last_modified_date:
                    # Save the object if it meets the suffix filtering requirement
                    qualifying_objects.append(
                        {
                            "key": content["Key"],
                            "size": content["Size"],
                            "last_modified": content["LastModified"],
                            "storage_class": content["StorageClass"],
                            "etag": content["ETag"],
                        }
                    )
    # Sort the objects by last_modified date in reverse order 
    qualifying_objects = sorted(qualifying_objects, key=lambda k: k["last_modified"],reverse=True)
    for obj in qualifying_objects:
        yield obj