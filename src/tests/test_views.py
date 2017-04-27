from unittest import mock

import pytest
from flask import url_for

from modifier import TMSetter


@pytest.fixture
def source_text():
    return 'Сейчас на фоне уязвимости Logjam все в индустрии в очередной раз обсуждают ' \
           'проблемы и особенности TLS. Я хочу воспользоваться этой возможностью, чтобы ' \
           'поговорить об одной из них, а именно — о настройке ciphersiutes.'

@pytest.fixture
def new_text():
    return 'Сейчас™ на фоне уязвимости Logjam™ все в индустрии в очередной раз обсуждают ' \
           'проблемы и особенности TLS. Я хочу воспользоваться этой возможностью, чтобы ' \
           'поговорить об одной из них, а именно™ — о настройке ciphersiutes.'


@pytest.fixture
def element():
    return mock.Mock(attrib={'href': 'https://habrahabr.ru/company/yandex/blog/258673/'})


def test_get_home_page(client):
    response = client.get(url_for('base'))
    assert response.status_code == 200
    assert '<!DOCTYPE html>' in str(response.data)


def test_proxy_by_path(client):
    response = client.get(url_for('proxy', path='/company/yandex/blog/258673/'))
    assert response.status_code == 200
    assert '<!DOCTYPE html>' in str(response.data)


def test_modify_text(source_text, new_text):
    result = TMSetter()._modify_text(source_text)
    assert result == new_text


def test_replace_link(element):
    TMSetter()._replace_link(
        element, 'http://habrahabr.ru/', 'http://127.0.0.1:8232/'
    )
    assert element.attrib['href'] == 'http://127.0.0.1:8232/company/yandex/blog/258673/'
