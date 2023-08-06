"""
  @Project     : sentry-dingtalk
  @Time        : 2021/07/12 17:34:35
  @File        : plugin.py
  @Author      : Jedore and Henryhaoson
  @Software    : VSCode
  @Desc        :
"""


import requests
import six
from sentry import tagstore
from sentry.plugins.bases import notify
from sentry.utils import json
from sentry.utils.http import absolute_uri
from sentry.integrations import FeatureDescription, IntegrationFeatures
from sentry_plugins.base import CorePluginMixin
from django.conf import settings


class DingTalkPlugin(CorePluginMixin, notify.NotificationPlugin):
    title = "DingTalk"
    slug = "dingtalk"
    description = "Post notifications to Dingtalk."
    conf_key = "dingtalk"
    required_field = "webhook"
    author = "Henryhaoson"
    author_url = "https://git.17bdc.com/android-apps/sentry-dingtalk"
    version = "9.0.0"
    resource_links = [
        ("Report Issue", "https://git.17bdc.com/android-apps/sentry-dingtalk/issues"),
        ("View Source", "https://git.17bdc.com/android-apps/sentry-dingtalk"),
    ]

    feature_descriptions = [
        FeatureDescription(
            """
                Configure rule based Dingtalk notifications to automatically be posted into a
                specific channel.
                """,
            IntegrationFeatures.ALERT_RULE,
        )
    ]

    def is_configured(self, project):
        return bool(self.get_option("webhook", project))

    def get_config(self, project, **kwargs):
        return [
            {
                "name": "webhook",
                "label": "webhook",
                "type": "url",
                "placeholder": "https://oapi.dingtalk.com/robot/send?access_token=**********",
                "required": True,
                "help": "钉钉 webhook 会@ 成员",
                "default": self.set_default(project, "webhook", "DINGTALK_WEBHOOK"),
            },
            {
                "name": "webhook_optional",
                "label": "webhook_optional",
                "type": "url",
                "placeholder": "https://oapi.dingtalk.com/robot/send?access_token=**********",
                "required": False,
                "help": "Optional - 可选 webhook， 不会 @成员",
                "default": self.set_default(
                    project, "webhook_optional", ""
                ),
            },
            {
                "name": "ats",
                "label": "@成员",
                "type": "string",
                "placeholder": "填写钉钉手机号",
                "required": False,
                "help": "Optional - 填写钉钉手机号，会 @ 对应成员",
                "default": self.set_default(
                    project, "ats", ""
                ),
            },
        ]

    def set_default(self, project, option, env_var):
        if self.get_option(option, project) != None:
            return self.get_option(option, project)
        if hasattr(settings, env_var):
            return six.text_type(getattr(settings, env_var))
        return None

    def notify(self, notification, raise_exception=False):
        event = notification.event
        user = event.get_minimal_user()
        user_id = user.id
        release = event.release
        group = event.group
        project = group.project
        self._post(group, user_id, release, project)

    def _post(self, group, userId, release, project):
        webhook = self.get_option("webhook", project)
        webhook_optional = self.get_option("webhook_optional", project)
        ats_str = self.get_option("ats", project)
        if ats_str == None:
            ats_str = ""
        ats_array = ats_str.split(",")
        ats_ding_str = ""
        for at in ats_array:
            ats_ding_str = f"{ats_ding_str} @{at} "

        issue_link = group.get_absolute_url(params={"referrer": "dingtalk"})
        release_link_path = issue_link.split("/issues/")[0]
        release_link = f"{release_link_path}/releases/{release}?project={project.id}"

        payload = f"## Error: [{group.title}>>]({issue_link}) \n\n"
        payload = f"{payload} #### UserId: [{userId}](https://admin.shanbay.com/jetty/users/{userId}) \n\n"
        payload = f"{payload} #### Project: {project.name} \n\n"
        payload = f"{payload} #### release: [{release}]({release_link}) \n\n"
        payload = f"{payload} #### event type: {group.get_event_type()} \n\n"
        payload = f"{payload} > Detail: {group.message} \n\n"

        headers = {
            "Content-type": "application/json",
            "Accept": "text/plain",
            "charset": "utf8"
        }

        data_optional = {
            "msgtype": "markdown",
            "markdown": {
                "title": group.title,
                "text": payload,
            },
        }
        # 可选 webhook，不会 @ 成员
        if len(webhook_optional) != 0:
            requests.post(webhook_optional, data=json.dumps(
                data_optional), headers=headers)

        # 必填 webhook，如果配置了 @ 成员，会执行
        payload = f"{payload} {ats_ding_str} \n\n"
        data = {
            "msgtype": "markdown",
            "markdown": {
                "title": group.title,
                "text": payload,
            },
            "at": {
                "atMobiles": ats_array,
                "isAtAll": "false"
            }
        }
        requests.post(webhook, data=json.dumps(data), headers=headers)
