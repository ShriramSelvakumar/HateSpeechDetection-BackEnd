import json
from django.http import JsonResponse, HttpResponse
import pandas as pd
from .models import Users
from sklearn.preprocessing import LabelEncoder
from NLP.ReadTwitterData import ReadTwitterData
import NLP.HSCNN as CNN
from django.views.decorators.csrf import csrf_exempt
import os


label_encoder = LabelEncoder()
label_encoder.fit(['NONE', 'PRFN', 'OFFN', 'HATE'], )
# consumer_key = 'boEJnpJF4kcfWSCDDHIpHjRL9'
# consumer_secret = 'YCWGzqe3MmjD1cBGKpEZoNp9ieuheJs4zp1CzYKR0JrQU4ePui'
# access_token = '406291233-uKGlGhDoPCvmO84ZQpKgDFjtOcbUYtSlQzwQFGFZ'
# access_token_secret = 'Nr7eMLJIoZcvllAX2rOCflj8bzsqcd4irNwDr1b1M8kdC'
# key = [consumer_key, consumer_secret, access_token, access_token_secret]
# twitter_api = ReadTwitterData(key)

@csrf_exempt
def new_user(request):
    if request.POST:
        if not request.session.exists(request.session.session_key):
            request.session.create()

        fields = ['consumer_key', 'consumer_secret', 'access_token', 'access_token_secret']
        consumer_key = request.POST.get("consumer_key", '')
        consumer_secret = request.POST.get("consumer_secret", '')
        access_token = request.POST.get("access_token", '')
        access_token_secret = request.POST.get("access_token_secret", '')
        user_session = request.session.session_key
        print([consumer_key, consumer_secret, access_token, access_token_secret, user_session])
        queryset = Users.objects.filter(user_session=user_session)
        if queryset.exists():
            user = queryset[0]
            user.consumer_key = consumer_key
            user.consumer_secret = consumer_secret
            user.access_token = access_token
            user.access_token_secret = access_token_secret
            user.save(update_fields=['consumer_key', 'consumer_secret', 'access_token', 'access_token_secret'])
            # a = pd.DataFrame([consumer_key, consumer_secret, access_token, access_token_secret], columns=fields)
            # return a.to_json()
            return JsonResponse({'message': 'Updated user', 'session_key': user_session})
        else:
            user = Users(user_session=user_session, consumer_key=consumer_key, consumer_secret=consumer_secret,
                         access_token=access_token, access_token_secret=access_token_secret)
            user.save()
            return JsonResponse({'message': 'Created User', 'session_key': user_session})
    return JsonResponse({'message': 'Something Went wrong'})


@csrf_exempt
def user_mentions_2(request):
    # Predict - New data
    user_session = request.POST.get("session_key", '')
    print(user_session)
    # return HttpResponse(user_session)
    queryset = Users.objects.filter(user_session=user_session)
    if queryset.exists():
        user = queryset[0]
        twitter_api = ReadTwitterData([user.consumer_key, user.consumer_secret,
                                       user.access_token, user.access_token_secret])
        print([user.consumer_key, user.consumer_secret, user.access_token, user.access_token_secret])
        count = request.POST.get("count", '')
        print([count])
        # return JsonResponse({'message': 'So far so good', 'session_key': user_session})
        twitter_data = twitter_api.get_user_mentions(count=int(count))
        predict_y_int = CNN.predict(twitter_data)
        predict_y = label_encoder.inverse_transform(predict_y_int)
        user_prediction = pd.DataFrame([False for x in range(0, len(predict_y))], columns=['user_prediction'])
        twitter_data = pd.concat([pd.DataFrame(predict_y, columns=['prediction']),
                                  user_prediction,
                                  twitter_data], axis=1)
        return JsonResponse(twitter_data.loc[:, ['text', 'screen_name', 'created_at',
                                                 'prediction', 'user_prediction']].to_dict())
    print('User Session does not exist')
    return JsonResponse({'message': 'Something Went wrong'})


@csrf_exempt
def search_tweets(request):
    # Predict - New data
    user_session = request.POST.get("session_key", '')
    print(user_session)
    # return HttpResponse(user_session)
    queryset = Users.objects.filter(user_session=user_session)
    if queryset.exists():
        user = queryset[0]
        twitter_api = ReadTwitterData([user.consumer_key, user.consumer_secret,
                                       user.access_token, user.access_token_secret])
        print([user.consumer_key, user.consumer_secret, user.access_token, user.access_token_secret])
        count = request.POST.get("count", '')
        lang = request.POST.get("lang", '')
        q = request.POST.get("query", '')
        print([count])
        print([lang])
        print([q])
        # return JsonResponse({'message': 'So far so good', 'session_key': user_session})
        twitter_data = twitter_api.search_tweets(q=q, lang=lang, count=int(count))
        predict_y_int = CNN.predict(twitter_data)
        predict_y = label_encoder.inverse_transform(predict_y_int)
        user_prediction = pd.DataFrame([False for x in range(0, len(predict_y))], columns=['user_prediction'])
        twitter_data = pd.concat([pd.DataFrame(predict_y, columns=['prediction']),
                                  user_prediction,
                                  twitter_data], axis=1)
        return JsonResponse(twitter_data.loc[:, ['text', 'screen_name', 'created_at',
                                                 'prediction', 'user_prediction']].to_dict())
    print('User Session does not exist')
    return JsonResponse({'message': 'Something Went wrong'})


@csrf_exempt
def export_tweets(request):
    # Exporting data to csv
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    user_session = body['session_key']
    tweets = body['tweets']
    tweets = pd.DataFrame(tweets.values(), columns=['tweets'])
    user_session = pd.DataFrame([user_session for x in range(0, len(tweets))], columns=['user_session'])
    ml_prediction = body['ml_prediction']
    ml_prediction = pd.DataFrame(ml_prediction.values(), columns=['ml_prediction'])
    save_both = body['save_both']
    if save_both:
        user_prediction = body['user_prediction']
        user_prediction = pd.DataFrame(user_prediction.values(), columns=['user_prediction'])
    else:
        user_prediction = pd.DataFrame(['NA' for x in range(0, len(tweets))], columns=['user_prediction'])
    twitter_data = pd.concat([user_session, tweets, ml_prediction,
                              user_prediction], axis=1)
    # Save File to /Data/Exported_Twitter_Data.csv file
    if os.path.exists('./Data/Exported_Twitter_Data.csv'):
        print('Path Exists')
        twitter_data.to_csv('./Data/Exported_Twitter_Data.csv', mode='a', index=False, header=False)
    else:
        print('Created New File')
        if not os.path.exists('./Data/'):
            os.mkdir('./Data/')
        twitter_data.to_csv('./Data/Exported_Twitter_Data.csv', mode='a', index=False)
    print('So far so good')
    return JsonResponse({'message': 'So far so good'})


@csrf_exempt
def block_users_json(request):
    # Exporting data to csv
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    user_session = body['session_key']
    name = body['name']
    name = pd.DataFrame(name.values(), columns=['name'])
    user_session = pd.DataFrame([user_session for x in range(0, len(name))], columns=['user_session'])
    use_user_predictions = body['use_user_predictions']
    if use_user_predictions:
        user_prediction = body['user_prediction']
        user_prediction = pd.DataFrame(user_prediction.values(), columns=['user_prediction'])
        twitter_data = pd.concat([user_session, name, user_prediction], axis=1)
        block_ids = twitter_data[twitter_data.loc[:, 'user_prediction'] == True].index
        block_users = twitter_data.loc[block_ids, ['name']]['name'].unique()
    else:
        ml_prediction = body['ml_prediction']
        ml_prediction = label_encoder.transform(ml_prediction.values())
        ml_prediction = pd.DataFrame(ml_prediction, columns=['ml_prediction'])
        twitter_data = pd.concat([user_session, name, ml_prediction], axis=1)
        block_ids = twitter_data[twitter_data.loc[:, 'ml_prediction']<=1].index
        block_users = twitter_data.loc[block_ids, ['name']]['name'].unique()
    # Block user(s)
    print('----------------------')
    print(block_users)
    print('----------------------')
    queryset = Users.objects.filter(user_session=body['session_key'])
    if queryset.exists():
        print('Test-----------------------')
        user = queryset[0]
        twitter_api = ReadTwitterData([user.consumer_key, user.consumer_secret,
                                       user.access_token, user.access_token_secret])
        twitter_api.block_users(block_users)
    print('So far so good')
    return JsonResponse({'message': 'So far so good'})


@csrf_exempt
def mute_users_json(request):
    # Exporting data to csv
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    user_session = body['session_key']
    name = body['name']
    name = pd.DataFrame(name.values(), columns=['name'])
    user_session = pd.DataFrame([user_session for x in range(0, len(name))], columns=['user_session'])
    use_user_predictions = body['use_user_predictions']
    if use_user_predictions:
        user_prediction = body['user_prediction']
        user_prediction = pd.DataFrame(user_prediction.values(), columns=['user_prediction'])
        twitter_data = pd.concat([user_session, name, user_prediction], axis=1)
        mute_ids = twitter_data[twitter_data.loc[:, 'user_prediction'] == True].index
        mute_users = twitter_data.loc[mute_ids, ['name']]['name'].unique()
    else:
        ml_prediction = body['ml_prediction']
        ml_prediction = label_encoder.transform(ml_prediction.values())
        ml_prediction = pd.DataFrame(ml_prediction, columns=['ml_prediction'])
        twitter_data = pd.concat([user_session, name, ml_prediction], axis=1)
        mute_ids = twitter_data[twitter_data.loc[:, 'ml_prediction']<=1].index
        mute_users = twitter_data.loc[mute_ids, ['name']]['name'].unique()
    # Block user(s)
    print('----------------------')
    print(mute_users)
    print('----------------------')
    queryset = Users.objects.filter(user_session=body['session_key'])
    if queryset.exists():
        print('Test-----------------------')
        user = queryset[0]
        twitter_api = ReadTwitterData([user.consumer_key, user.consumer_secret,
                                       user.access_token, user.access_token_secret])
        twitter_api.mute_users(mute_users)
    print('So far so good')
    return JsonResponse({'message': 'So far so good'})












