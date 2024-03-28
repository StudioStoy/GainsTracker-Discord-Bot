import logging

from Infrastructure.BaseCommand import BaseCommand
from Common.Constants import GAINS_URL
from Common.Methods import getDataFromResponse

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format='%(message)s')


class GetAvailableNewWorkoutsRequest(BaseCommand):
    def __init__(self, interaction):
        super().__init__(interaction)

    async def execute(self):
        session = await self.sessionCenter.get_session()
        workoutsResponse = session.get(f"{GAINS_URL}/catalog/workout")

        if not self.responsePositive(workoutsResponse):
            await self.checkStatusCode(workoutsResponse)
            return

        return getDataFromResponse(workoutsResponse)
