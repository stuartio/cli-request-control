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


    def list_policy_versions(self, session, policy_id, page_size='optional'):
        """
        Function to fetch a cloudlet policy versions

        Parameters
        -----------
        session : <string>
            An EdgeGrid Auth akamai session object

        Returns
        -------
        cloudletPolicyResponse : cloudletPolicyResponse
            Json object details of specific cloudlet policy versions
        """
        if page_size == 'optional':
            cloudlet_policy_versions_url = 'https://' + self.access_hostname + \
                                           '/cloudlets/api/v2/policies/' + str(
                                               policy_id) + '/versions?includeRules=true'
        else:
            cloudlet_policy_versions_url = 'https://' + self.access_hostname + '/cloudlets/api/v2/policies/' + \
                                           str(policy_id) + '/versions?includeRules=true&pageSize=' + page_size
        cloudlet_policy_versions_response = session.get(
            cloudlet_policy_versions_url)
        return cloudlet_policy_versions_response


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
            session,
            policy_id,
            policy_details,
            version):
        """
        Function to update a policy version

        Parameters
        -----------
        session : <string>
            An EdgeGrid Auth akamai session object

        Returns
        -------
        cloudlet_policy_update_response : cloudlet_policy_update_response
            Json object details of updated cloudlet policy version
        """
        headers = {
            "Content-Type": "application/json"
        }
        cloudlet_policy_update_url = 'https://' + self.access_hostname + '/cloudlets/api/v2/policies/' + \
                                     str(policy_id) + '/versions/' + str(version) + '?omitRules=false'
        cloudlet_policy_update_response = session.put(
            cloudlet_policy_update_url, data=policy_details, headers=headers)
        return cloudlet_policy_update_response

    def activate_policy_version(
            self,
            session,
            policy_id,
            version,
            network='staging'):
        """
        Function to activate a policy version

        Parameters
        -----------
        session : <string>
            An EdgeGrid Auth akamai session object

        Returns
        -------
        cloudlet_policy_activate_response : cloudlet_policy_activate_response
            Json object details of activated cloudlet policy version
        """
        headers = {
            "Content-Type": "application/json"
        }
        network_data = """{
            "network" : "%s"
        }""" % network
        cloudlet_policy_activate_url = 'https://' + self.access_hostname + \
            '/cloudlets/api/v2/policies/' + str(policy_id) + '/versions/' + str(version) + '/activations'
        cloudlet_policy_activate_response = session.post(
            cloudlet_policy_activate_url, data=network_data, headers=headers)
        return cloudlet_policy_activate_response

    def delete_policy_version(self, session, policy_id, version):
        """
        Function to delete a policy version

        Parameters
        -----------
        session : <string>
            An EdgeGrid Auth akamai session object

        Returns
        -------
        cloudlet_policy_delete_response : cloudlet_policy_delete_response
            Json object details of deleted cloudlet policy version
        """

        cloudlet_policy_delete_url = 'https://' + self.access_hostname + \
                                     '/cloudlets/api/v2/policies/' + str(policy_id) + '/versions/' + str(version)
        cloudlet_policy_delete_response = session.delete(
            cloudlet_policy_delete_url)
        return cloudlet_policy_delete_response
