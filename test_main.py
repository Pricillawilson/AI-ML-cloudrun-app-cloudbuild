import pytest
from unittest.mock import patch, MagicMock
from main import app

@pytest.fixture
def client():
    """Flask test client."""
    with app.test_client() as client:
        yield client

@patch('main.get_bigquery_client')
def test_main_endpoint(mock_get_bigquery_client, client):
    """Test the main endpoint with mocked BigQuery client."""
    # Mock BigQuery client methods
    mock_bigquery_client = MagicMock()
    mock_get_bigquery_client.return_value = mock_bigquery_client

    mock_load_job = MagicMock()
    mock_bigquery_client.load_table_from_uri.return_value = mock_load_job
    mock_load_job.result.return_value = None

    mock_table = MagicMock()
    mock_table.num_rows = 50
    mock_bigquery_client.get_table.return_value = mock_table

    # Test the endpoint
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert 'data' in data
    assert data['data'] == 50

    # Verify mocked methods were called
    mock_bigquery_client.load_table_from_uri.assert_called_once()
    mock_load_job.result.assert_called_once()
    mock_bigquery_client.get_table.assert_called_once_with("ml-project-161098.test_schema.us_states")
