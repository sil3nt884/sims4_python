from situations.base_situation import _RequestUserData
class AmbientSimSpecificCustomStatesSituation(CustomStatesSituation):

    def _issue_requests(self):
        request = SpecificSimRequestFactory(self, _RequestUserData(), self.default_job(), BouncerRequestPriority.EVENT_DEFAULT_JOB, self.exclusivity, self._guest_list.host_sim_id)
        self.manager.bouncer.submit_request(request)
