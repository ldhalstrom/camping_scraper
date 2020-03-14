"""CAMPING SCRAPER OBJECTS
"""

class CampReservation
    """ Class definition for a specific desired camping reservation
    """


    def __init__(self,
                 name=None,
                 date_start=None,
                 length_stay=1,
                 website=None,
                 campground=None,
                 browser='Chrome',
                 verbose=0,
                 debug=0,
                 ):
        """ Constructor for camping reservation object

        Computes stay interval dates
        Gets specific URL for reservation website + campground

        Args:
            name  (:obj:`string`): Name of trip (Default: Campground and Date) [None]
            date_start (:obj:`string`): Date of first night of stay (Default: Today) [None]
            length_stay (:obj:`int`): Number of nights you will stay [1]
            website (:obj:`string`): Keyword for reservation website [None]
            campground (:obj:`string`): Keyword for desired campground [None]
            browser (:obj:`string`): Web browser to use for scraping ['Chrome']
            verbose (:obj:`bool`): Pring incremental steps to screen [0]
            debug (:obj:`bool`): Debug check and output flag [0]

        """

        #GET STAY INTERVAL
            #formatted in datetime
        self.length_stay = length_stay
        self.date_start, self.date_end = GetStayInterval(date_start, length_stay)

        #GET CAMPGROUND URL
        self.website = website
        self.campground = campground
        self.url = '{}/{}'.format(urls[website], campIDs[campground])



        #GET DRIVER FOR WEB BROWSER
        self.headless = False if debug else True
        self.browser = browser
        if self.browser == 'Chrome':
            self.driver = GetWebDriver_Chrome(headless=self.headless)
        elif self.browser == 'Firefox':
            self.driver = GetWebDriver_Firefox(headless=self.headless)
        else:
            raise ValueError('No driver for this web browser')




class ResScraper
    """ Class definition for a website scraper for camping reservation
    """


    def __init__(self,
                 name=None,
                 stateparams=None,
                 atype=None,
                 verbose=0,
                 debug=0,
                 ):
        """ Constructor for trajectory reconstruction Algorithm object.

        Specifies name for this trajectory reconstruction algorithm instance.
        Sets atmospheric state parameters to reconstruct.
        Sets screen output settings for verbose and debug modes.
        Specific algorithm methodologies must be set after this initialization.

        Args:
            name  (:obj:`string`): Name for the algorithm [None]
            stateparams (:obj:`list`): List of trajectory state variables [None]
            atype (:obj:`string`): Keyword for algorithm family [None]
            verbose (:obj:`bool`): Incremental algorithm steps printed to screen [0]
            debug (:obj:`bool`): Debug check and output flag [0]

        """
