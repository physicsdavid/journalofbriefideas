import json
from cStringIO import StringIO

import requests
from requests_oauthlib import OAuth1

from figshare_credentials import (
    consumer_key,
    consumer_secret,
)

HEADERS = {'content-type':'application/json'}

def get_name_from_figshare_id(figshare_id):
    res = requests.get("http://figshare.com/authors/Unknown/%s" % figshare_id)
    #XXX replace with lxml or beautifulsoup
    #XXX or ask them to make an API call for this (unless i missed it)
    name = res.content.split('id="author_name">')[1].split("<", 1)[0]
    return name

#XXX: i was getting an "incorrect base string" API response when using flask-oauthlib
#XXX: could only get the API calls to work by manually creating the OAuth1 client
#XXX: need to go back through the flask-oauthlib examples and make sure i'm sending oauth_token_secret

class FigshareClient(object):
    def __init__(self, key, secret):
        self.oauth = OAuth1(
            client_key=consumer_key,
            client_secret=consumer_secret,
            resource_owner_key=key,
            resource_owner_secret=secret,
            signature_type='auth_header'
        )
        self.client = requests.session()

    def post_article(self, title, description):
        body = {'title':title, 'description': description, 'defined_type': 'paper'}
        res = self.client.post('http://api.figshare.com/v1/my_data/articles', auth=self.oauth, data=json.dumps(body), headers=HEADERS)
        res = json.loads(res.content)
        return res['article_id']

    def attach_idea_as_file(self, art_id, idea_text):
        files = {'filedata': ('idea.txt', StringIO(idea_text))}
        res = self.client.put('http://api.figshare.com/v1/my_data/articles/%s/files' % art_id, auth=self.oauth, files=files)
        res = json.loads(res.content)
        return res

    def add_category(self, art_id, cat_id):
        body = {'category_id': cat_id}
        res = self.client.put('http://api.figshare.com/v1/my_data/articles/%s/categories' % art_id, auth=self.oauth, data=json.dumps(body), headers=HEADERS)
        res = json.loads(res.content)
        return res

    def add_tag(self, art_id, tag_name="Journal of Brief Ideas"):
        body = {'tag_name': tag_name}
        res = self.client.put('http://api.figshare.com/v1/my_data/articles/%s/tags' % art_id, auth=self.oauth, data=json.dumps(body), headers=HEADERS)
        res = json.loads(res.content)
        return res

    def make_public(self, art_id):
        res = self.client.post('http://api.figshare.com/v1/my_data/articles/%s/action/make_public' % art_id, auth=self.oauth, headers=HEADERS)
        res = json.loads(res.content)
        return res

    def get_article(self, art_id):
        res = self.client.get('http://api.figshare.com/v1/articles/%s' % art_id, auth=self.oauth)
        res = json.loads(res.content)
        return res

    def get_big_ideas(self, n=4):
        #XXX: don't have time to implement this, just returning some sample data
        #XXX: we need persistence in the app and voting / citation tracking in order
        #XXX: to determine the popularity of things posted through our site

        ideas = [
            {"title": "Radio Detection of A Candidate Neutron Star",
                "category": "Astrophysics", "idea_text": "We report the VLA detection of the radio counterpart of the X-ray object referred to as the \"Cannonball\", which has been proposed to be the remnant neutron star resulting from the creation of the Galactic Center supernova remnant, Sagittarius A East. The radio object was detected both in our new VLA image from observations in 2012 at 5.5 GHz and in archival VLA images from observations in 1987 at 4.75 GHz and in the period from 1990 to 2002 at 8.31 GHz. The radio morphology of this object is characterized as a compact, partially resolved point source located at the northern tip of a radio \"tongue\" similar to the X-ray structure observed by Chandra. Behind the Cannonball, a radio counterpart to the X-ray plume is observed. This object consists of a broad radio plume with a size of 30\\arcsec$\\times$15\\arcsec, followed by a linear tail having a length of 30\\arcsec. The compact head and broad plume sources appear to have relatively flat spectra ($\\propto\\nu^\\alpha$) with mean values of $\\alpha=-0.44\\pm0.08$ and $-0.10\\pm0.02$, respectively; and the linear tail shows a steep spectrum with the mean value of $-1.94\\pm0.05$. Ref: arXiv:1309.7020"},
            {"title": "Top as a veto in astrophysical neutrino searches for IceCube",
                "category": "Astrophysics", "idea_text": "IceCube, the world's largest high-energy neutrino observatory, was built at the South Pole. It consists of photomultipliers deployed 1.5-2.5 km deep into the Antarctic ice cap and detects the trajectory of charged leptons produced during high-energy neutrino interactions in the surrounding ice. The surface air shower detector IceTop located above IceCube can be used to veto the cosmic ray induced background in IceCube to measure astrophysical neutrinos from the southern sky. The implementation of the IceTop veto technique and the impact on different IceCube analyses are presented. Ref: arXiv:1309.7010"},
            {"title": "Herschel observations and a model for IRAS 08572+3915",
                "category": "Astrophysics", "idea_text": "We present Herschel photometry and spectroscopy, carried out as part of the Herschel ULIRG survey (HERUS), and a model for the infrared to submillimetre emission of the ultraluminous infrared galaxy IRAS 08572+3915. This source shows one of the deepest known silicate absorption features and no polycyclic aromatic hydrocarbon (PAH) emission. The model suggests that this object is powered by an active galactic nucleus (AGN) with a fairly smooth torus viewed almost edge-on and a very young starburst. According to our model the AGN contributes about 90% of the total luminosity of 1.1 x 10^13 Lo, which is about a factor of five higher than previous estimates. The large correction of the luminosity is due to the anisotropy of the emission of the best fit torus. Similar corrections may be necessary for other local and high-z analogs. This correction implies that IRAS 08572+3915 at a redshift of 0.05835 may be the nearest hyperluminous infrared galaxy and probably the most luminous infrared galaxy in the local (z < 0.2) Universe. Ref: arXiv:1309.7005"},
            {"title": "The optical transmission spectrum of the hot Jupiter HAT-P-32b",
                "category": "Astrophysics", "idea_text": "We report Gemini-North GMOS observations of the inflated hot Jupiter HAT-P-32b during two primary transits. We simultaneously observed two comparison stars and used differential spectro-photometry to produce multi-wavelength light curves. 'White' light curves and 29 'spectral' light curves were extracted for each transit and analysed to refine the system parameters and produce transmission spectra from 520-930nm in ~14nm bins. The light curves contain time-varying white noise as well as time-correlated noise, and we used a Gaussian process model to fit this complex noise model. Common mode corrections derived from the white light curve fits were applied to the spectral light curves which significantly improved our precision, reaching typical uncertainties in the transit depth of ~2x10^-4, corresponding to about half a pressure scale height. The low resolution transmission spectra are consistent with a featureless model, and we can confidently rule out broad features larger than about one scale height. The absence of Na/K wings or prominent TiO/VO features is most easily explained by grey absorption from clouds in the upper atmosphere, masking the spectral features. Ref: arXiv:1309.6998"},
            {"title": "XIPE: the X-ray Imaging Polarimetry Explorer",
                "category": "Astrophysics", "idea_text": "X-ray polarimetry, sometimes alone, and sometimes coupled to spectral and temporal variability measurements and to imaging, allows a wealth of physical phenomena in astrophysics to be studied. X-ray polarimetry investigates the acceleration process, for example, including those typical of magnetic reconnection in solar flares, but also emission in the strong magnetic fields of neutron stars and white dwarfs. It detects scattering in asymmetric structures such as accretion disks and columns, and in the so-called molecular torus and ionization cones. In addition, it allows fundamental physics in regimes of gravity and of magnetic field intensity not accessible to experiments on the Earth to be probed. Finally, models that describe fundamental interactions (e.g. quantum gravity and the extension of the Standard Model) can be tested. We describe in this paper the X-ray Imaging Polarimetry Explorer (XIPE), proposed in June 2012 to the first ESA call for a small mission with a launch in 2017 but not selected. Ref: arXiv:1309.6995"},
            {"title": "Overview of the SOFIA Data Cycle System",
                "category": "Astrophysics", "idea_text": "The Stratospheric Observatory for Infrared Astronomy (SOFIA) is an airborne astronomical observatory comprised of a 2.5 meter infrared telescope mounted in the aft section of a Boeing 747SP aircraft that flies at operational altitudes between 37,000 and 45,00 feet, above 99% of atmospheric water vapor. During routine operations, a host of instruments will be available to the astronomical community including cameras and spectrographs in the near- to far-IR; a sub-mm heterodyne receiver; and an high-speed occultation imager. One of the challenges for SOFIA (and all observatories in general) is providing a uniform set of tools that enable the non-expert General Investigator (GI) to propose, plan, and obtain observations using a variety of very different instruments in an easy and seamless manner. The SOFIA Data Cycle System (DCS) is an integrated set of services and user tools for the SOFIA Science and Mission Operations GI Program designed to address this challenge. Ref: arXiv:1309.6994"},
            {"title": "Orbital Parameters for the Two Young Binaries VSB 111 and VSB 126",
                "category": "Astrophysics", "idea_text": "We report orbital parameters for two low-mass, pre-main sequence, double-lined spectroscopic binaries VSB 111 and VSB 126. These systems were originally identified as single-lined on the basis of visible-light observations. We obtained high-resolution, infrared spectra with the 10-m Keck II telescope, detected absorption lines of the secondary stars, and measured radial velocities of both components in the systems. The visible light spectra were obtained on the 1.5-m Wyeth reflector at the Oak Ridge Observatory, the 1.5-m Tillinghast reflector at the F. L. Whipple Observatory, and the 4.5-m equivalent Multiple Mirror Telescope. The combination of our visible and infrared observations of VSB 111 leads to a period of 902.1+/-0.9 days, an eccentricity of 0.788+/-0.008, and a mass ratio of 0.52+/-0.05. VSB 126 has a period of 12.9244+/-0.0002 days, an eccentricity of 0.18+/-0.02, and a mass ratio of 0.29+/-0.02. Visible-light photometry, using the 0.8-m telescope at Lowell Observatory, provided rotation periods for the primary stars in both systems, 3.74+/-0.02 days for VSB 111 and 5.71+/-0.07 days for VSB 126.  Ref: arXiv:1309.6985"},
            {"title": "How Cold is Cold Dark Matter?",
                "category": "Astrophysics", "idea_text": "If cold dark matter consists of particles, these must be non-interacting and non-relativistic by definition. In most cold dark matter models, however, dark matter particles inherit a non-vanishing velocity dispersion from interactions in the early universe, a velocity that redshifts with cosmic expansion but certainly remains non-zero. In this article, we place model-independent constraints on the dark matter temperature to mass ratio, whose square root determines the dark matter velocity dispersion. We only assume that dark matter particles decoupled kinetically while non-relativistic, when galactic scales had not entered the horizon yet, and that their momentum distribution has been Maxwellian since that time. Under these assumptions, using cosmic microwave background and matter power spectrum observations, we place upper limits on the temperature to mass ratio of cold dark matter. The latter imply that its velocity dispersion extrapolated to the present has to be smaller than 56 m/s. Cold dark matter has to be quite cold, indeed. Ref: arXiv:1309.6971"},
            {"title": "Stellar Magnetic Dynamos and Activity Cycles",
                "category": "Astrophysics", "idea_text": "Using a new uniform sample of 824 solar and late-type stars with measured X-ray luminosities and rotation periods we have studied the relationship between rotation and stellar activity that is believed to be a probe of the underlying stellar dynamo. Using an unbiased subset of the sample we calculate the power law slope of the unsaturated regime of the activity -- rotation relationship as $L_X/L_{bol}\\propto Ro^\\beta$, where $\\beta=-2.70\\pm0.13$. This is inconsistent with the canonical $\\beta = -2$ slope to a confidence of 5$\\sigma$ and argues for an interface-type dynamo. We map out three regimes of coronal emission as a function of stellar mass and age, using the empirical saturation threshold and theoretical super-saturation thresholds. We find that the empirical saturation timescale is well correlated with the time at which stars transition from the rapidly rotating convective sequence to the slowly rotating interface sequence in stellar spin-down models. This may be hinting at fundamental changes in the underlying stellar dynamo or internal structure. Ref: arXiv:1309.6970"},
            {"title": "Studying the Molecular Ambient towards the Young Stellar Object EGO G35.04-0.47",
                "category": "Astrophysics", "idea_text": "We are performing a systematic study of the interstellar medium around extended green objects (EGOs), likely massive young stellar objects driving outflows. EGO G35.04-0.47 is located towards a dark cloud at the northern-west edge of an HII region. Recently, H2 jets were discovered towards this source, mainly towards its southwest, where the H2 1-0 S(1) emission peaks. Therefore, the source was catalogued as the Molecular Hydrogen emission-line object MHO 2429. In order to study the molecular ambient towards this star-forming site, we observed a region around the aforementioned EGO using the Atacama Submillimeter Telescope Experiment in the 12CO J=3--2, 13CO J=3--2, HCO+ J=4--3, and CS J=7--6 lines with an angular and spectral resolution of 22\" and 0.11 km s-1, respectively. The observations revealed a molecular clump where the EGO is embedded at v_LSR ~ 51 km s-1, in coincidence with the velocity of a Class I 95 GHz methanol maser previously detected. Analyzing the 12CO line we discovered high velocity molecular gas in the range from 34 to 47 km s-1, most likely a blueshifted outflow driven by the EGO. Ref: arXiv:1309.6962"}
        ]
        for i in ideas:
            i['id'] = '999999' #???
        import random
        random.shuffle(ideas)
        ideas = ideas[:n-1]

        #we'll include one real result at the top for us to click on in the demo
        ideas.insert(0, {
            "title": "Computational Complexity of Sudoku Solving Strategies",
            "category": "Applied Computer Science",
            "id": "810457",
            "idea_text": '''Found through analysis of common sudoku solving algorithms.
                Singles:
                O(R*C*V) =
                O(N^3)
                Hidden singles (section, row, and column-wise):
                O(U1*U2*V) =
                O(N^3)
                Naked pairs:
                O(R*C*(V+R*C*(2*V+3*U*V))) =
                O(N^6)
                Pointing pair triples (row and column-wise):
                O(V*S*((SC*SR)+S)) =
                O(N^3)
                Box line reduction (row and column-wise):
                O(V*U*(2*SC*SR)) =
                O(N^3)
                Hidden pairs (section, row, and column-wise):
                O(U1*V*U2*V*U2*V) =
                O(N^6)
                Guess & backtrack:
                O(N^N)'''
        })
        return ideas

    def search(self, query):
        #XXX: re-use example data from get_big_ideas to stub out the search functionality
        #XXX: the figshare search API looks very easy to use though:
        #XXX: http://api.figshare.com/docs/howto.html#how-do-i-search-for-an-article-what-filters-are-available
        #XXX: just search for the query plus the "Journal of Big Ideas" tag
        ideas = self.get_big_ideas(n=9999)
        ideas = [i for i in ideas if query.lower() in repr(i).lower()]
        return dict(results=ideas)
