from django.test import TestCase
from unittest import mock
from chess_app.models import Game
from users.models import Profile
from django.contrib.auth.models import User
from datetime import datetime, timedelta, timezone
import humanize


class GameTestCase(TestCase):
    """
    Test Module for Game Model
    """
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(
            username='auth_user', email='test@email.com', password='test1234')

        anon_user = Profile.objects.create(
            session_id="anon_user")
        anon_user2 = Profile.objects.create(
            session_id="anon_user2")

    def setUp(self):
        self.auth_user = Profile.objects.get(sanitized_name='auth_user')
        self.anon_user = Profile.objects.get(sanitized_name='anon_user')
        self.anon_user2 = Profile.objects.get(sanitized_name='anon_user2')
        live_game = Game.objects.create(
            creator=self.anon_user,
            openGame=False,
            opponent=self.auth_user,
        )
        completed_game = Game.objects.create(
            creator=self.auth_user,
            opponent=self.anon_user,
            created=datetime(2015, 2, 1, 0, 0, tzinfo=timezone.utc),
            completed=datetime(2015, 2, 1, 0, 0, tzinfo=timezone.utc),
        )
        open_game = Game.objects.create(creator=self.auth_user)

        live_game.save()
        completed_game.save()
        open_game.save()

    def test_get_all_open_games(self):
        self.assertEqual(Game.get_all_open_games().count(), 1)

    def test_created_count(self):
        self.assertEqual(Game.created_count(self.auth_user), 2)

    def test_get_completed(self):
        self.assertEqual(Game.get_completed(self.auth_user).count(), 1)

    def test_get_live(self):
        self.assertEqual(Game.get_live(self.auth_user).count(), 1)

    def test_get_by_id(self):
        game = Game.get_completed(self.auth_user).first()
        match_id = game.match_id
        assert Game.get_by_id(match_id).creator == self.auth_user \
            and Game.get_by_id(match_id).match_id == match_id \
            and Game.get_by_id(match_id).completed == datetime(2015, 2, 1, 0, 0,
                                                               tzinfo=timezone.utc)

    def test_create_new(self):
        new_game = Game.create_new(self.anon_user2)
        new_game.save()
        self.assertEqual(Game.created_count(self.anon_user2), 1)

    def test_get_length(self):
        mocked = datetime(2015, 2, 1, 0, 0, 0, tzinfo=timezone.utc)
        with mock.patch('django.utils.timezone.now', mock.Mock(return_value=mocked)):
            game = Game.create_new(self.auth_user)
            game.completed = datetime(2015, 2, 2, 0, 0, tzinfo=timezone.utc)
            game.save()
            self.assertEqual(game.get_length(),
                             humanize.naturaldelta(timedelta(days=1)))

    def test_time_since(self):
        game = Game.get_completed(self.auth_user).first()
        self.assertEqual(game.time_since(datetime(
            2015, 2, 2, 0, 0, tzinfo=timezone.utc)), humanize.naturaltime(timedelta(days=1)))

    def test_mark_complete(self):
        game = Game.get_live(self.auth_user).first()
        game.completed = datetime.now(timezone.utc)
        game.save()
        self.assertEqual(game.get_completed(self.auth_user).count(), 2)
