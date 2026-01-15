import sendpost_python_sdk
from sendpost_python_sdk.api import EmailApi
from sendpost_python_sdk.models import EmailMessageObject, EmailAddress, Recipient
import os
import re
from typing import List, Dict, Any, Optional, Union

class SendPostEmailService:
    def __init__(self):
        self.api_key = os.getenv('SENDPOST_API_KEY')
        self.from_email = os.getenv('SENDPOST_FROM_EMAIL', 'hello@playwithsendpost.io')
        self.from_name = os.getenv('SENDPOST_FROM_NAME', 'SendPost')
        self.configuration = sendpost_python_sdk.Configuration(
            host="https://api.sendpost.io/api/v1"
        )
        self.configuration.api_key['subAccountAuth'] = self.api_key
    
    async def send_email(
        self,
        to: Union[str, List[Union[str, Dict[str, Any]]]],
        subject: str,
        html_body: str,
        text_body: Optional[str] = None,
        from_email: Optional[str] = None,
        from_name: Optional[str] = None,
        groups: Optional[List[str]] = None,
        track_opens: bool = True,
        track_clicks: bool = True,
        custom_fields: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        try:
            with sendpost_python_sdk.ApiClient(self.configuration) as api_client:
                email_message = EmailMessageObject()
                
                email_message.var_from = EmailAddress(
                    email=from_email or self.from_email,
                    name=from_name or self.from_name
                )
                
                if isinstance(to, str):
                    recipients = [Recipient(email=to)]
                elif isinstance(to, list):
                    recipients = []
                    for recipient in to:
                        if isinstance(recipient, str):
                            recipients.append(Recipient(email=recipient))
                        elif isinstance(recipient, dict):
                            recipients.append(Recipient(
                                email=recipient.get('email'),
                                name=recipient.get('name'),
                                custom_fields=recipient.get('customFields') or custom_fields
                            ))
                        else:
                            recipients.append(recipient)
                else:
                    recipients = [Recipient(email=to)]
                
                email_message.to = recipients
                email_message.subject = subject
                email_message.html_body = html_body
                email_message.text_body = text_body or self._html_to_text(html_body)
                email_message.track_opens = track_opens
                email_message.track_clicks = track_clicks
                
                if groups:
                    email_message.groups = groups if isinstance(groups, list) else [groups]
                
                response = EmailApi(api_client).send_email(email_message)[0]
                
                return {
                    'success': True,
                    'message_id': response.message_id,
                    'data': response
                }
        except sendpost_python_sdk.exceptions.ApiException as e:
            return {
                'success': False,
                'message_id': None,
                'error': f"API Error {e.status}: {e.body}"
            }
        except Exception as e:
            return {
                'success': False,
                'message_id': None,
                'error': str(e)
            }
    
    def _html_to_text(self, html: str) -> str:
        text = re.sub(r'<[^>]+>', '', html)
        text = text.replace('&nbsp;', ' ')
        text = text.replace('&amp;', '&')
        text = text.replace('&lt;', '<')
        text = text.replace('&gt;', '>')
        return text.strip()
