"""
Copyright 2017 Akamai Technologies, Inc. All Rights Reserved.

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""

import json
from http_calls import EdgeGridHttpCaller


class Cloudlet(object):
    def __init__(self, config):
        self.http_caller = EdgeGridHttpCaller(config, False, False)


    def list_cloudlet_groups(self):
        """
        Returns information about the Cloudlet types associated with the groups you have edit privileges for.

        Parameters
        -----------
            None

        Returns
        -------
            (result) Object with cloudlet types associated with the groups
        """
        endpoint = '/cloudlets/api/v2/group-info'
        result = self.http_caller.getResult(endpoint)
        return (result)


    def list_policies(
            self,
            group_id = None,
            cloudlet_id = None):
        """
        Returns cloudlet policies associated with group_id

        Parameters
        -----------
            group Id,
            cloudlet Id
        Returns
        -------
            (result) Policies of cloudlet Id
        """
        endpoint = '/cloudlets/api/v2/policies'
        result = self.http_caller.getResult(endpoint, {"gid": group_id, "cloudletId": cloudlet_id})
        return (result)


    def get_cloudlet_policy(self, policy_id, version = None):
        endpoint = '/cloudlets/api/v2/policies/' + str(policy_id)
        if version:
            endpoint += '/versions/' + version
        
        result = self.http_caller.getResult(endpoint, {})
        return (result)

        # if version == 'optional':
        #     cloudlet_policy_url = 'https://' + self.access_hostname + \
        #                           '/cloudlets/api/v2/policies/' + str(policy_id)
        # else:
        #     cloudlet_policy_url = 'https://' + self.access_hostname + '/cloudlets/api/v2/policies/' + \
        #                           str(policy_id) + '/versions/' + str(version) + '?omitRules=false'
        # cloudlet_policy_response = session.get(cloudlet_policy_url)
        
        return result


    def create_policy_version(
            self,
            policy_id,
            clone_version = None,
            policy_data = {}):
        
        endpoint = '/cloudlets/api/v2/policies/' + str(policy_id) + '/versions'
        result = self.http_caller.postResult(endpoint, policy_data, {'includeRules': 'true', 'cloneVersion': clone_version})
        return (result)


    def update_policy_version(
            self,
            policy_id,
            policy_details,
            version):
        
        endpoint = '/cloudlets/api/v2/policies/' + str(policy_id) + '/versions/' + str(version) + '?omitRules=false'
        # refactoring not finished
        cloudlet_policy_update_response = session.put(
            cloudlet_policy_update_url, data=policy_details, headers=headers)
        return cloudlet_policy_update_response


    def activate_policy_version(
            self,
            policy_id,
            version,
            network='staging'):
        """
        Function to activate a policy version
        """

        data = """{
            "network" : "%s"
        }""" % network

        endpoint = '/cloudlets/api/v2/policies/' + str(policy_id) + '/versions/' + str(version) + '/activations'
        result = self.http_caller.postResult(endpoint, data, {})
        return (result)
        

    def add_rule(
            self,
            policy_id,
            version,
            index = None,
            rule_data = {}):
        
        endpoint = '/cloudlets/api/v2/policies/' + str(policy_id) + '/versions/'+ str(version) +'/rules'
        result = self.http_caller.postResult(endpoint, rule_data, {'index': index})
        return (result)

    def modify_rule(
            self,
            policy_id,
            version,
            rule_id,
            # index = None,
            rule_data = {}):
        
        endpoint = '/cloudlets/api/v2/policies/' + str(policy_id) + '/versions/'+ str(version) +'/rules/' + str(rule_id)
        result = self.http_caller.putResult(endpoint, rule_data, {})
        return (result)
