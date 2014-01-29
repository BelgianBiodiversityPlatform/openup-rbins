import time

import gdata.analytics.client
from gdata.sample_util import CLIENT_LOGIN, SettingsUtil

GA_MINIMAL_DATE = '2005-01-01'
GA_TODAY_DATE = time.strftime("%Y-%m-%d")


def ga_metrics(ga_app_name, ga_user_email, ga_user_pass, ga_table_id):
    """Query the Google Analytics API and returns {'visits': X, 'visitors':Y}."""

    gdata_client = gdata.analytics.client.AnalyticsClient(source=ga_app_name)

    # Login
    settings_util = SettingsUtil(prefs={"email": ga_user_email,
                                        "password": ga_user_pass})

    settings_util.authorize_client(gdata_client,
                                   service=gdata_client.auth_service,
                                   auth_type=CLIENT_LOGIN,
                                   source=ga_app_name,
                                   scopes=['https://www.google.com/analytics/feeds/'])

    data_query = gdata.analytics.client.DataFeedQuery({'ids': ga_table_id,
                                                       'start-date': GA_MINIMAL_DATE,
                                                       'end-date': GA_TODAY_DATE,
                                                       'metrics': 'ga:visits, ga:visitors',
                                                       'output': 'dataTable'})

    feed = gdata_client.GetDataFeed(data_query)

    return {'visitors': feed.aggregates.get_metric('ga:visitors').value,
            'visits': feed.aggregates.get_metric('ga:visits').value}
