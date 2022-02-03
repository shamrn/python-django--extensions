
VOXIMPLANT = {
    'URL': 'https://api.voximplant.com/platform_api/StartScenarios/',
    'ACCOUN_ID': int,
    'API_KEY': '',
    'RULE_ID': int,  # the routing section of the site
}


def voximplant_send(phones):

    if not phones:
        return

    virequest = '%s?%s' % (VOXIMPLANT['URL'], urlencode({
        'account_id': VOXIMPLANT['ACCOUN_ID'],
        'api_key': VOXIMPLANT['API_KEY'],
        'rule_id': VOXIMPLANT['RULE_ID'],
        'script_custom_data': phones,
    }),)
    urlopen(virequest)

phones = ['+7999900000', '+79999909999', '+79999909999']

phones = ':'.join(i.lstrip('+') for i in phones)

voximplant_send(phones)
