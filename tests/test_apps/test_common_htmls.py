from http import HTTPStatus

import pytest
from django.template.defaultfilters import escape
from django.template.loader import render_to_string
from django.test import Client
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed


@pytest.mark.django_db()
def test_index_template(
    as_user_client: Client,
) -> None:
    """Test the index template."""
    response = as_user_client.get(reverse('index'))
    template = 'pictures/pages/index.html'

    assert response.status_code == HTTPStatus.OK
    assertTemplateUsed(response, template)


def test_messages_template() -> None:
    """Test the message template."""
    data_test_id = 'data-test-id="message"'
    context = {'messages': [data_test_id]}
    response = render_to_string('common/includes/messages.html', context)

    assert escape(data_test_id) in response


def test_base_template() -> None:
    """Test the base template."""
    response = render_to_string('common/_base.html', {})

    assert response
