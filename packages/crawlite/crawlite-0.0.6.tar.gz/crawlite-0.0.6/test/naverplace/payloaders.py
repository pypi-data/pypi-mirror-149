import json


def gen_naver_place_comment_payloader(place_id, page, count_per_page):
    request_template = '''
        [{"operationName":"getVisitorReviews","variables":{"input":{"businessId":"1784206724","businessType":"restaurant","item":"0","bookingBusinessId":"75411","page":4,"display":100,"isPhotoUsed":false,"includeContent":true,"getAuthorInfo":true,"includeReceiptPhotos":true,"cidList":["220036","220038","220081","220804","1004760","1004452"]},"id":"676217924"},"query":"query getVisitorReviews($input: VisitorReviewsInput) {  visitorReviews(input: $input) {    items {      id      rating      author {        id        nickname        from        imageUrl        objectId        url        review {          totalCount          imageCount          avgRating          __typename        }        theme {          totalCount          __typename        }        __typename      }      body      thumbnail      media {        type        thumbnail        class        __typename      }      tags      status      visitCount      viewCount      visited      created      reply {        editUrl        body        editedBy        created        replyTitle        __typename      }      originType      item {        name        code        options        __typename      }      language      highlightOffsets      apolloCacheId      translatedText      businessName      showBookingItemName      showBookingItemOptions      bookingItemName      bookingItemOptions      votedKeywords {        code        iconUrl        iconCode        displayName        __typename      }      userIdno      isFollowing      followerCount      followRequested      loginIdno      __typename    }    starDistribution {      score      count      __typename    }    hideProductSelectBox    total    showRecommendationSort    __typename  }}"}]
    '''
    req = json.loads(request_template)
    # print(req[0]['variables']['input'])
    req[0]['variables']['input']['businessId'] = place_id
    req[0]['variables']['input']['page'] = page
    req[0]['variables']['input']['display'] = count_per_page
    req = json.dumps(req)
    return req

