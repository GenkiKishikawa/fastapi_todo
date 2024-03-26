import pytest
import pytest_asyncio
import starlette.status

from tests.test_main import async_client


@pytest.mark.asyncio
async def test_done_flag(async_client):
	response = await async_client.post("/tasks", json={"title": "テストタスク2"})
	assert response.status_code == starlette.status.HTTP_200_OK
	response_obj = response.json()
	assert response_obj["title"] == "テストタスク2"

	# 完了フラグを立てる
	response = await async_client.put("/tasks/1/done")
	assert response.status_code == starlette.status.HTTP_200_OK

	# 既に完了フラグが立っているので400を返却
	response = await async_client.put("/tasks/1/done")
	assert response.status_code == starlette.status.HTTP_400_BAD_REQUEST

	# 完了フラグを外す
	response = await async_client.delete("/tasks/1/done")
	assert response.status_code == starlette.status.HTTP_200_OK

	# 既に完了フラグが外れているので400を返却
	response = await async_client.delete("/tasks/1/done")
	assert response.status_code == starlette.status.HTTP_404_NOT_FOUND