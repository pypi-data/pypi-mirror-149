# Copyright 2021 ONDEWO GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import grpc
import os
from dataclasses import dataclass
from typing import List, Optional, Dict, Any

from ondewo.nlu import context_pb2
from ondewo.vtsi import call_log_pb2, call_log_pb2_grpc, voip_pb2, voip_pb2_grpc


@dataclass
class VtsiConfiguration:
    """location of voip server"""
    host: str = "grpc-vtsi.ondewo.com"
    port: int = 443
    secure: bool = False
    cert_path: str = ''


def create_parameter_dict(my_dict: Dict) -> Optional[Dict[str, context_pb2.Context.Parameter]]:
    assert isinstance(my_dict, dict) or my_dict is None, "parameter must be a dict or None"
    if my_dict is not None:
        return {
            key: context_pb2.Context.Parameter(
                display_name=key,
                value=my_dict[key]
            )
            for key in my_dict
        }
    return None


class VtsiClient:
    """
    exposes the endpoints of the ondewo voip-server in a user-friendly way
    """

    def __init__(self,
                 config_voip: VtsiConfiguration
                 ) -> None:
        self.config_voip = config_voip

        target = f"{self.config_voip.host}:{self.config_voip.port}"

        # create grpc service stub
        if self.config_voip.secure:

            if os.path.exists(self.config_voip.cert_path):
                with open(self.config_voip.cert_path, "rb") as fi:
                    grpc_cert = fi.read()

            credentials = grpc.ssl_channel_credentials(root_certificates=grpc_cert)
            channel = grpc.secure_channel(target, credentials)
            print(f'Creating a secure channel to {target}')
        else:
            channel = grpc.insecure_channel(target=target)
            print(f'Creating an insecure channel to {target}')
        self.voip_stub = voip_pb2_grpc.VoipSessionsStub(channel=channel)
        self.call_log_stub = call_log_pb2_grpc.VoipCallLogsStub(channel=channel)

    def stop_call(
            self, call_id: Optional[str] = None, sip_id: Optional[str] = None,
    ) -> bool:
        """
        stop an ongoing call
        """
        return self._stop_call(call_id=call_id, sip_id=sip_id)

    def _stop_call(
            self, call_id: Optional[str] = None, sip_id: Optional[str] = None,
    ) -> bool:
        """
        stop a call instance
        """
        if call_id:
            request = voip_pb2.StopCallInstanceRequest(call_id=call_id)
        elif sip_id:
            request = voip_pb2.StopCallInstanceRequest(sip_id=sip_id)
        else:
            raise ValueError("either call_id or sip_id needs to be specified!")
        print("stopping call")
        response: voip_pb2.StopCallInstanceResponse = self.voip_stub.StopCallInstance(request=request)
        return response.success  # type: ignore

    def start_call_instance_request(self, start_call_instance_requests: voip_pb2.StartCallInstanceRequest
                                    ) -> voip_pb2.StartCallInstanceResponse:

        return self.voip_stub.StartCallInstance(request=start_call_instance_requests)

    def start_multiple_call_instances(self,
                                      start_call_instance_requests: voip_pb2.StartMultipleCallInstancesRequest):
        return self.voip_stub.StartMultipleCallInstances(request=start_call_instance_requests)

    def get_instance_status(self, call_id: Optional[str] = None,
                            sip_id: Optional[str] = None, ) -> voip_pb2.VoipStatus:
        """
        stop a listener instance
        """
        if call_id:
            request = voip_pb2.GetVoipStatusRequest(call_id=call_id)
        elif sip_id:
            request = voip_pb2.GetVoipStatusRequest(sip_id=sip_id)
        else:
            raise ValueError("either call_id or sip_id needs to be specified!")
        print("getting instance status")
        response: voip_pb2.VoipStatus = self.voip_stub.GetInstanceStatus(request=request)
        return response

    def update_services_status(
            self, call_id: Optional[str] = None, sip_id: Optional[str] = None,
            manifest_id: Optional[str] = None,
    ) -> voip_pb2.UpdateServicesStatusResponse:
        """
        send update requests to speech-to-text, asterisk, text-to-speech and cai, which can then be retrieved by
            get_instance_status() or
            get_manifest_status()
        """
        if call_id:
            request = voip_pb2.UpdateServicesStatusRequest(call_id=call_id)
        elif sip_id:
            request = voip_pb2.UpdateServicesStatusRequest(sip_id=sip_id)
        elif manifest_id:
            request = voip_pb2.UpdateServicesStatusRequest(manifest_id=manifest_id)
        else:
            raise ValueError("either call_id, sip_id or manifest_id needs to be specified!")
        print("updating services' status")
        response: voip_pb2.UpdateServicesStatusResponse = self.voip_stub.UpdateServicesStatus(request=request)
        return response

    def get_call_ids(self) -> List[str]:
        """
        get all call_ids known to the voip manager
        """
        request = voip_pb2.GetCallIDsRequest()
        response: voip_pb2.GetCallIDsResponse = self.voip_stub.GetCallIDs(request=request)
        call_ids = []
        for call_id in response.call_ids:
            call_ids.append(call_id)
        return call_ids

    def get_session_id(self, call_id: str) -> str:
        """
        get session id by call id
        """
        request = voip_pb2.GetSessionIDRequest(
            call_id=call_id
        )
        response: voip_pb2.GetSessionIDResponse = self.voip_stub.GetSessionID(request=request)
        return response.session_id

    def shutdown_unhealthy_calls(self) -> bool:
        """
        shutdown any deployed call instances with unhealthy overall voip status
        """
        request = voip_pb2.ShutdownUnhealthyCallsRequest()
        response: voip_pb2.ShutdownUnhealthyCallsResponse = self.voip_stub.ShutdownUnhealthyCalls(
            request=request)
        return response.success  # type: ignore

    def get_voip_log(self, call_id: str) -> call_log_pb2.GetVoipLogResponse:
        """
        get the call log of a sip-sim instance
        """
        request = call_log_pb2.GetVoipLogRequest(call_id=call_id)
        response: call_log_pb2.GetVoipLogResponse = self.call_log_stub.GetVoipLog(request=request)
        return response

    def get_audio_file(self, request: voip_pb2.GetAudioFileRequest) -> voip_pb2.GetAudioFileResponse:
        return self.voip_stub.GetAudioFile(request=request)

    def get_full_conversation_audio_file(self, request: voip_pb2.GetFullConversationAudioFileRequest) \
            -> voip_pb2.GetFullConversationAudioFileResponse:
        return self.voip_stub.GetFullConversationAudioFile(request=request)
