import grpc

from userwatch import userwatch_shepherd_pb2
from userwatch import userwatch_shepherd_pb2_grpc


class Userwatch:
    shepherd = None
    privateApiKey = None

    def __init__(self, privateApiKey, options = {}):
        url = options.get("url", "api.userwat.ch:443")
        self.privateApiKey = privateApiKey
        channel = None
        if options.get("insecure", False):
            channel = grpc.insecure_channel(url)
        else:
            channel = grpc.secure_channel(
                url,
                grpc.ssl_channel_credentials()
            )
        self.shepherd = userwatch_shepherd_pb2_grpc.ShepherdStub(channel)

    def validate(self,
                 reportToken,  # string
                 userInfo, # userwatch_public_pb2.UserInfo
                 eventType,  # userwatch_public_pb2.EventType
                 challengeVerification=None):  # optional userwatch_shepherd_pb2.ChallengeVerificationRequest
        return self.shepherd.Validate(
            userwatch_shepherd_pb2.ValidationRequest(
                validation_token=reportToken,
                userinfo=userInfo,
                event_type=eventType,
                challenge_verification=challengeVerification,
            ),
            metadata=[("x-api-key", self.privateApiKey)]
        )

    def createChallenge(self,
                        type,  # userwatch_public_pb2.ChallengeType
                        userInfo,  # userwatch_public_pb2.UserInfo
                        deviceId,  # string
                        origin=None  # Optional. Required for webauthn Should be consistent eg. login.company.com or similar
                        ):
        return self.shepherd.CreateChallenge(
            userwatch_shepherd_pb2.CreateChallengeRequest(
                type=type,
                userinfo=userInfo,
                device_id=deviceId,
                origin=origin
            ),
            metadata=[("x-api-key", self.privateApiKey)]
        )

    def verifyChallenge(
            self,
            type, # userwatch_public_pb2.ChallengeType
            userInfo, # userwatch_public_pb2.UserInfo
            deviceId, # string
            challengeId, # string
            secretResponse # string, eg the sms code.
        ):
        return self.shepherd.VerifyChallenge(
            userwatch_shepherd_pb2.ChallengeVerificationRequest(
                type=type,
                userinfo = userInfo,
                device_id=deviceId,
                challenge_id=challengeId,
                secret_response=secretResponse
            ),
            metadata=[("x-api-key", self.privateApiKey)]
        )

    # def reportDevice(self, userId, deviceId):
    #     return self.shepherd.reportDevice(
    #         userId=userId,
    #         deviceId=deviceId,
    #         global
    #     )

    # def approveDevice(self, userId, deviceId):
    #     return self.shepherd.approveDevice(
    #         userId=userId,
    #         deviceId=deviceId,
    #         global
    #     )

    def getDeviceList(self, userId):
        return self.shepherd.GetDeviceList(
            userwatch_shepherd_pb2.DeviceListRequest(user_id=userId),
            metadata=[("x-api-key", self.privateApiKey)]
        )
