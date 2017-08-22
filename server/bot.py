# -*- coding: utf-8 -*-


class ChatBot(object):

    # Handlers
    def handle_feedback(self):
        return {"message": "Thank you for participating our feedback survey."}

    # Getters
    def get_feedback(self):
        actions = [
            {
                "text": "Yes",
                "type": "button",
                "value": "yes",
                "style": "success",
                "is_disabled_on_selection": True,
                "is_disabled_on_visitor_message": False
            },
            {
                "text": "I don't know",
                "type": "button",
                "value": "maybe",
                "is_disabled_on_selection": True,
                "is_disabled_on_visitor_message": False
            },
            {
                "text": "No",
                "type": "button",
                "value": "no",
                "style": "danger",
                "is_disabled_on_selection": True,
                "is_disabled_on_visitor_message": False
            }
        ]
        attachments = [{
            "text": "Was this conversation helpful?",
            "actions": actions
        }]
        message = {"message": "We would like to hear your feedback about this conversation", "attachments": attachments}
        return message

    def get_numeric_feedback(self):
        actions = [
            {
                "text": "1",
                "type": "button",
                "value": "1",
                "style": "info",
                "is_disabled_on_selection": True,
                "is_disabled_on_visitor_message": False
            },
            {
                "text": "2",
                "type": "button",
                "value": "2",
                "style": "info",
                "is_disabled_on_selection": True,
                "is_disabled_on_visitor_message": False
            },
            {
                "text": "3",
                "type": "button",
                "value": "3",
                "style": "info",
                "is_disabled_on_selection": True,
                "is_disabled_on_visitor_message": False
            },
            {
                "text": "4",
                "type": "button",
                "value": "4",
                "style": "info",
                "is_disabled_on_selection": True,
                "is_disabled_on_visitor_message": False
            },
            {
                "text": "5",
                "type": "button",
                "value": "5",
                "style": "info",
                "is_disabled_on_selection": True,
                "is_disabled_on_visitor_message": False
            },
        ]
        attachments = [{
            "text": "From 1 to 5, how would you rate this conversation?",
            "actions": actions
        }]
        message = {"message": "We would like to hear your feedback about this conversation.", "attachments": attachments}
        return message

    def get_jacket_suggestions(self, gender):
        if gender == 'female':
            attachments = [
                {
                    "title": "Peak performance women's jacket",
                    "title_link_url": "https://www.bfgcdn.com/1500_1500_90/104-0643/peak-performance-womens-heli-gravity-jacket-ski-jacket.jpg",
                    "text": "Warm winter jacket, 220€"
                },
                {
                    "title": "North Face women's jacket",
                    "title_link_url": "https://images.evo.com/imgp/700/55292/308857/the-north-face-freedom-jacket-women-s-barberry-pink-front.jpg",
                    "text": "Waterproof winter jacket, 160€"
                },
                {
                    "title": "Haglöfs women's jacket",
                    "title_link_url": "https://planet-sports-res.cloudinary.com/images/t_ps_xl/planetsports/products/39121000_00/hagloefs-couloir-iv-snowboard-jacket-women-red.jpg",
                    "text": "Warm winter jacket, 200€"
                }
            ]

        else:
            attachments = [
                {
                    "title": "Peak performance men's jacket",
                    "title_link_url": "http://demandware.edgesuite.net/aarw_prd/on/demandware.static/-/Sites-master-catalog-pp/default/dw8ae22bcc/zoom/G58685037_050_main.png",
                    "text": "Warm winter jacket, 250€"
                },
                {
                    "title": "North Face men's jacket",
                    "title_link_url": "https://ta-tnf.s3.amazonaws.com/product/A8ARKX7_1_xlarge.jpg",
                    "text": "Waterproof winter jacket, 180€"
                },
                {
                    "title": "Haglöfs men's jacket",
                    "title_link_url": "https://www.outdoorxl.com/media/catalog/product/cache/default/image/9df78eab33525d08d6e5fb8d27136e95/h/a/haglofs-bliss-jacket-men-s-gale-blue-1.png",
                    "text": "Warm winter jacket, 210€"
                }
            ]
        message = {"message": "Here are my three suggestions for you.", "attachments": attachments}
        return message
