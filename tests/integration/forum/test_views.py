
from flask import url_for
from flask_login import login_user
from flaskbb.forum.models import Forum, Topic

# CoRise TODO: implement a integration test to validate the functionality of post method
"""
Hint: All actions require an logged in user autorized to manage topics the super_moderator_user
matches that criteria. Additionally, you will need access to a forum and topic both exist as a fixture.

Additionally, you will need a topic and a forum both are available as fixtures. Finally, you will need to
turn of cross site scripting checks since you are not using a real browser.

Your can use this template for each integration test you write.

def test_<action>(application, forum, topic, super_moderator_user):
    application.config['WTF_CSRF_ENABLED'] = False

    with application.test_client() as test_client:
        manage_forum_url = url_for("forum.manage_forum", forum_id=forum.id)

        login_response = test_client.post(url_for('auth.login'), data={'login': super_moderator_user.username,
                                        'password': 'test'},
                        follow_redirects=True)

        response = test_client.post(manage_forum_url, data = {
            "rowid": topic.id,
            ...
        }, follow_redirects=True)

        assert response.status_code == 200

    fresh_topic = Topic.query.filter_by(id=topic.id).first()
    # validate topic state change here.

"""

def test_lock(application, forum, topic, super_moderator_user):
    application.config['WTF_CSRF_ENABLED'] = False

    assert topic.locked is False

    with application.test_client() as test_client:
        manage_forum_url = url_for("forum.manage_forum", forum_id=forum.id)

        login_response = test_client.post(url_for('auth.login'), data={'login': super_moderator_user.username,
                                                                       'password': 'test'},
                                          follow_redirects=True)

        response = test_client.post(manage_forum_url, data={
            "rowid": topic.id,
            "lock": "1"
        }, follow_redirects=True)

        assert response.status_code == 200

    fresh_topic = Topic.query.filter_by(id=topic.id).first()
    assert fresh_topic.locked is True

def test_unlock(application, forum, topic, super_moderator_user):
    application.config['WTF_CSRF_ENABLED'] = False

    setattr(topic, "locked", True)
    topic.save()
    assert topic.locked is True

    with application.test_client() as test_client:
        manage_forum_url = url_for("forum.manage_forum", forum_id=forum.id)

        login_response = test_client.post(url_for('auth.login'), data={'login': super_moderator_user.username,
                                                                       'password': 'test'},
                                          follow_redirects=True)

        response = test_client.post(manage_forum_url, data={
            "rowid": topic.id,
            "unlock": "1"
        }, follow_redirects=True)

        assert response.status_code == 200

    fresh_topic = Topic.query.filter_by(id=topic.id).first()
    assert fresh_topic.locked is False

def test_highlight(application, forum, topic, super_moderator_user):
    application.config['WTF_CSRF_ENABLED'] = False

    assert topic.important is False

    with application.test_client() as test_client:
        manage_forum_url = url_for("forum.manage_forum", forum_id=forum.id)

        login_response = test_client.post(url_for('auth.login'), data={'login': super_moderator_user.username,
                                                                       'password': 'test'},
                                          follow_redirects=True)

        response = test_client.post(manage_forum_url, data={
            "rowid": topic.id,
            "highlight": "1"
        }, follow_redirects=True)

        assert response.status_code == 200

    fresh_topic = Topic.query.filter_by(id=topic.id).first()
    assert fresh_topic.important is True

def test_trivialize(application, forum, topic, super_moderator_user):
    application.config['WTF_CSRF_ENABLED'] = False

    setattr(topic, "important", True)
    topic.save()
    assert topic.important is True

    with application.test_client() as test_client:
        manage_forum_url = url_for("forum.manage_forum", forum_id=forum.id)

        login_response = test_client.post(url_for('auth.login'), data={'login': super_moderator_user.username,
                                                                       'password': 'test'},
                                          follow_redirects=True)

        response = test_client.post(manage_forum_url, data={
            "rowid": topic.id,
            "trivialize": "1"
        }, follow_redirects=True)

        assert response.status_code == 200

    fresh_topic = Topic.query.filter_by(id=topic.id).first()
    assert fresh_topic.important is False

def test_delete(application, forum, topic, super_moderator_user):
    application.config['WTF_CSRF_ENABLED'] = False

    with application.test_client() as test_client:
        manage_forum_url = url_for("forum.manage_forum", forum_id=forum.id)

        login_response = test_client.post(url_for('auth.login'), data={'login': super_moderator_user.username,
                                                                       'password': 'test'},
                                          follow_redirects=True)

        response = test_client.post(manage_forum_url, data={
            "rowid": topic.id,
            "delete": "1"
        }, follow_redirects=True)

        assert response.status_code == 200

    fresh_topic = Topic.query.filter_by(id=topic.id).first()
    assert fresh_topic is None

def test_move(application, forum, topic, category, default_groups, super_moderator_user):
    application.config['WTF_CSRF_ENABLED'] = False

    new_forum = Forum(title="Second Test Forum", category_id=category.id)
    new_forum.groups = default_groups
    new_forum.save()

    assert not topic.forum == new_forum

    with application.test_client() as test_client:
        manage_forum_url = url_for("forum.manage_forum", forum_id=forum.id)

        login_response = test_client.post(url_for('auth.login'), data={'login': super_moderator_user.username,
                                                                       'password': 'test'},
                                          follow_redirects=True)

        response = test_client.post(manage_forum_url, data={
            "rowid": topic.id,
            "move": "1",
            "forum": new_forum.id
        }, follow_redirects=True)

        assert response.status_code == 200

    fresh_topic = Topic.query.filter_by(id=topic.id).first()
    assert fresh_topic.forum == new_forum

def test_hide(application, forum, topic, super_moderator_user):
    application.config['WTF_CSRF_ENABLED'] = False

    assert topic.hidden is False

    with application.test_client() as test_client:
        manage_forum_url = url_for("forum.manage_forum", forum_id=forum.id)

        login_response = test_client.post(url_for('auth.login'), data={'login': super_moderator_user.username,
                                                                       'password': 'test'},
                                          follow_redirects=True)

        response = test_client.post(manage_forum_url, data={
            "rowid": topic.id,
            "hide": "1"
        }, follow_redirects=True)

        assert response.status_code == 200

    fresh_topic = Topic.query.with_hidden().filter_by(id=topic.id).first()
    assert fresh_topic.hidden is True

def test_unhide(application, forum, topic, super_moderator_user):
    application.config['WTF_CSRF_ENABLED'] = False

    setattr(topic, "hidden", True)
    topic.save()
    assert topic.hidden is True

    with application.test_client() as test_client:
        manage_forum_url = url_for("forum.manage_forum", forum_id=forum.id)

        login_response = test_client.post(url_for('auth.login'), data={'login': super_moderator_user.username,
                                                                       'password': 'test'},
                                          follow_redirects=True)

        response = test_client.post(manage_forum_url, data={
            "rowid": topic.id,
            "unhide": "1"
        }, follow_redirects=True)

        assert response.status_code == 200

    fresh_topic = Topic.query.filter_by(id=topic.id).first()
    assert fresh_topic.hidden is False
