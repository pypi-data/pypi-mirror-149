from diffusion.internal.services.abstract import OutboundService
from diffusion.internal.serialisers import get_serialiser
from diffusion.internal.services.topics import (
    NotifySubscription,
    AddAndSetTopic,
    TopicAdd,
    NotifyUnsubscription,
    Unsubscribe,
    Subscribe,
    TopicRemoval,
)
from diffusion.internal.services.session import UserPing, ChangePrincipal, SystemPing
from diffusion.internal.services.messaging import (
    MessagingFilterSender,
    MessagingReceiverServer,
    MessagingReceiverClient,
    MessagingReceiverControlRegistration,
    MessagingSend,
    FilterResponse,
)
import attr


class SetTopic(OutboundService):
    service_id = 118
    name = "SET_TOPIC"
    request_serialiser_map = {
        15: "set-topic-request",
        16: "set-topic-request",
        22: "set-topic-request",
    }
    response_serialiser_map = {15: "void", 16: "void", 22: "void"}
    request_serialiser = get_serialiser("set-topic-request")
    response_serialiser = get_serialiser("void")


class PutSessionMetricCollector(OutboundService):
    service_id = 135
    name = "PUT_SESSION_METRIC_COLLECTOR"
    request_serialiser_map = {
        16: "protocol16-session-metric-collector",
        22: "protocol16-session-metric-collector",
        24: "session-metric-collector",
    }
    response_serialiser_map = {
        16: "error-report-list",
        22: "error-report-list",
        24: "error-report-list",
    }
    request_serialiser = get_serialiser("session-metric-collector")
    response_serialiser = get_serialiser("error-report-list")


class RemoveSessionMetricCollector(OutboundService):
    service_id = 136
    name = "REMOVE_SESSION_METRIC_COLLECTOR"
    request_serialiser_map = {16: "string", 22: "string"}
    response_serialiser_map = {16: "void", 22: "void"}
    request_serialiser = get_serialiser("string")
    response_serialiser = get_serialiser("void")


class ListSessionMetricCollectors(OutboundService):
    service_id = 137
    name = "LIST_SESSION_METRIC_COLLECTORS"
    request_serialiser_map = {16: "void", 22: "void", 24: "void"}
    response_serialiser_map = {
        16: "protocol16-session-metric-collectors",
        22: "protocol16-session-metric-collectors",
        24: "session-metric-collectors",
    }
    request_serialiser = get_serialiser("void")
    response_serialiser = get_serialiser("session-metric-collectors")


class PutTopicMetricCollector(OutboundService):
    service_id = 146
    name = "PUT_TOPIC_METRIC_COLLECTOR"
    request_serialiser_map = {
        16: "protocol16-topic-metric-collector",
        22: "protocol16-topic-metric-collector",
        24: "topic-metric-collector",
    }
    response_serialiser_map = {16: "void", 22: "void", 24: "void"}
    request_serialiser = get_serialiser("topic-metric-collector")
    response_serialiser = get_serialiser("void")


class RemoveTopicMetricCollector(OutboundService):
    service_id = 147
    name = "REMOVE_TOPIC_METRIC_COLLECTOR"
    request_serialiser_map = {16: "string", 22: "string"}
    response_serialiser_map = {16: "void", 22: "void"}
    request_serialiser = get_serialiser("string")
    response_serialiser = get_serialiser("void")


class ListTopicMetricCollectors(OutboundService):
    service_id = 148
    name = "LIST_TOPIC_METRIC_COLLECTORS"
    request_serialiser_map = {16: "void", 22: "void", 24: "void"}
    response_serialiser_map = {
        16: "protocol16-topic-metric-collectors",
        22: "protocol16-topic-metric-collectors",
        24: "topic-metric-collectors",
    }
    request_serialiser = get_serialiser("void")
    response_serialiser = get_serialiser("topic-metric-collectors")


class PutBranchMappingTable(OutboundService):
    service_id = 176
    name = "PUT_BRANCH_MAPPING_TABLE"
    request_serialiser_map = {22: "branch-mapping-table"}
    response_serialiser_map = {22: "void"}
    request_serialiser = get_serialiser("branch-mapping-table")
    response_serialiser = get_serialiser("void")


class GetSessionTreeBranchesWithMappings(OutboundService):
    service_id = 177
    name = "GET_SESSION_TREE_BRANCHES_WITH_MAPPINGS"
    request_serialiser_map = {22: "void"}
    response_serialiser_map = {22: "session-tree-branch-list"}
    request_serialiser = get_serialiser("void")
    response_serialiser = get_serialiser("session-tree-branch-list")


class GetBranchMappingTable(OutboundService):
    service_id = 178
    name = "GET_BRANCH_MAPPING_TABLE"
    request_serialiser_map = {22: "string"}
    response_serialiser_map = {22: "branch-mapping-table"}
    request_serialiser = get_serialiser("string")
    response_serialiser = get_serialiser("branch-mapping-table")


@attr.s(auto_attribs=True)
class ServiceLocatorStatic(object):
    SUBSCRIBE: Subscribe = Subscribe()
    UNSUBSCRIBE: Unsubscribe = Unsubscribe()
    CHANGE_PRINCIPAL: ChangePrincipal = ChangePrincipal()
    NOTIFY_UNSUBSCRIPTION: NotifyUnsubscription = NotifyUnsubscription()
    SYSTEM_PING: SystemPing = SystemPing()
    USER_PING: UserPing = UserPing()
    TOPIC_REMOVAL: TopicRemoval = TopicRemoval()
    MESSAGING_SEND: MessagingSend = MessagingSend()
    MESSAGING_RECEIVER_SERVER: MessagingReceiverServer = MessagingReceiverServer()
    NOTIFY_SUBSCRIPTION: NotifySubscription = NotifySubscription()
    MESSAGING_RECEIVER_CLIENT: MessagingReceiverClient = MessagingReceiverClient()
    MESSAGING_RECEIVER_CONTROL_REGISTRATION: MessagingReceiverControlRegistration = (
        MessagingReceiverControlRegistration()
    )
    MESSAGING_FILTER_SENDER: MessagingFilterSender = MessagingFilterSender()
    FILTER_RESPONSE: FilterResponse = FilterResponse()
    TOPIC_ADD: TopicAdd = TopicAdd()
    SET_TOPIC: SetTopic = SetTopic()
    ADD_AND_SET_TOPIC: AddAndSetTopic = AddAndSetTopic()
    PUT_SESSION_METRIC_COLLECTOR: PutSessionMetricCollector = (
        PutSessionMetricCollector()
    )
    REMOVE_SESSION_METRIC_COLLECTOR: RemoveSessionMetricCollector = (
        RemoveSessionMetricCollector()
    )
    LIST_SESSION_METRIC_COLLECTORS: ListSessionMetricCollectors = (
        ListSessionMetricCollectors()
    )
    PUT_TOPIC_METRIC_COLLECTOR: PutTopicMetricCollector = PutTopicMetricCollector()
    REMOVE_TOPIC_METRIC_COLLECTOR: RemoveTopicMetricCollector = (
        RemoveTopicMetricCollector()
    )
    LIST_TOPIC_METRIC_COLLECTORS: ListTopicMetricCollectors = (
        ListTopicMetricCollectors()
    )
    PUT_BRANCH_MAPPING_TABLE: PutBranchMappingTable = PutBranchMappingTable()
    GET_SESSION_TREE_BRANCHES_WITH_MAPPINGS: GetSessionTreeBranchesWithMappings = (
        GetSessionTreeBranchesWithMappings()
    )
    GET_BRANCH_MAPPING_TABLE: GetBranchMappingTable = GetBranchMappingTable()
