from flask import url_for

from app.post.models import Category, Post


def test_create_post(client, init_database, log_in_user, categories, tags):
    data = {
        'title': 'New',
        'text': 'Some text',
        'category': categories[0].id,
        'type': 'news',
        'tags': [tags[0].id],
    }

    response = client.post(url_for('post.create'), data=data, follow_redirects=True)

    post = Post.query.filter_by(title='New').first()

    assert response.status_code == 200
    assert post
    assert post.user_id == log_in_user.id
    assert b'Your post added successfully' in response.data

def test_get_all_posts(init_database):
    number_of_posts = Post.query.count()
    assert number_of_posts == 4


def test_edit_post(client, init_database, log_in_user, categories, tags, posts):
    post_to_update = posts[0]
    data = {
        'title': 'Edited',
        'text': post_to_update.text,
        'type': 'other',
        'enabled': post_to_update.enabled,
        'category': post_to_update.category_id,
        'tags': [tags[0].id, tags[1].id],
    }

    response = client.post(url_for('post.edit_post', post_id=post_to_update.id), data=data, follow_redirects=True)

    updated = Post.query.get(post_to_update.id)

    assert response.status_code == 200
    assert updated is not None
    assert updated.title == 'Edited'
    assert len(updated.tags) == 2
    assert 'Post updated successfully!' in response.text


def test_delete_post(client, init_database, log_in_user):
    response = client.post(
        url_for('post.delete_post', post_id=2),
        follow_redirects=True
    )
    deleted_post = Post.query.filter_by(id=2).first()
    assert response.status_code == 200
    assert deleted_post is None
    assert b'Post deleted successfully' in response.data


def test_categories_page(client):
    response = client.get(url_for('post.categories'))
    assert response.status_code == 200
    assert b'Categories' in response.data


def test_create_category(client, init_database, log_in_user):
    data = {
        'name': 'Test category',
    }

    response = client.post(url_for('post.categories'), data=data, follow_redirects=True)

    category = Category.query.filter_by(name=data['name']).first()

    assert response.status_code == 200
    assert category
    assert b'New category added successfully' in response.data


def test_edit_category(client, init_database, log_in_user, categories):
    category = categories[0]
    data = {
        'name': 'Edited name',
    }

    response = client.post(url_for('post.edit_category', category_id=category.id), data=data, follow_redirects=True)

    updated = Category.query.get(category.id)

    assert response.status_code == 200
    assert updated is not None
    assert updated.name == 'Edited name'
    assert b'Category has been updated!' in response.data


def test_delete_category(client, init_database, log_in_user, categories):
    category = categories[0]

    response = client.post(url_for('post.delete_category', category_id=category.id), follow_redirects=True)

    deleted_category = Category.query.filter_by(id=category.id).first()

    assert response.status_code == 200
    assert deleted_category is None