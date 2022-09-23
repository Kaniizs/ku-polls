"""This module contains a testcases for testing."""
import datetime

from django.test import TestCase, Client
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Question


def create_question(question_text, days):
    """Create a question with text and published offset to localtime."""
    time = timezone.localtime() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionModelTests(TestCase):
    """Testcase for question model."""

    def test_was_published_recently_with_future_question(self):
        """Returns False for questions whose pub_date is in the future."""
        time = timezone.localtime() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """Returns False for questions whose pub_dateis older than 1 day."""
        time = timezone.localtime() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """Returns True for questions whose pub_dateis within the last day."""
        lct = timezone.localtime()
        time = lct - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_is_published_with_future_question(self):
        """Returns False for questions whose pub_date is in the future."""
        time = timezone.localtime() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.is_published(), False)

    def test_is_published_with_old_question(self):
        """Returns False for questions whose pub_date is older than 1 day."""
        time = timezone.localtime() - datetime.timedelta(days=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.is_published(), True)

    def test_can_vote_within_pub_and_end_date(self):
        """Return True for questions whose can vote within date."""
        lct = timezone.localtime()
        pub_time = lct - datetime.timedelta(minutes=1)
        end_time = lct + datetime.timedelta(minutes=1)
        test_q = Question(pub_date=pub_time, end_date=end_time)
        self.assertTrue(test_q.can_vote())

    def test_can_vote_with_future_question(self):
        """Returns False for questions whose pub_date is in the future."""
        time = timezone.localtime() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.can_vote(), False)

    def test_can_vote_with_old_question(self):
        """Returns False for questions whose pub_dateis already passed."""
        time = timezone.localtime() - datetime.timedelta(days=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.can_vote(), True)

    def test_can_vote_with_expired_quesiton(self):
        """Returns False for questions whose end_dateis already over."""
        time = timezone.localtime() - datetime.timedelta(days=1)
        expired_question = Question(end_date=time)
        self.assertIs(expired_question.can_vote(), False)

    def test_can_vote_without_end_date_question(self):
        """Returns True for questions whose not have end_date."""
        time = timezone.localtime()
        no_end_date_ques = Question(pub_date=time)
        self.assertIs(no_end_date_ques.can_vote(), True)


class VoteModelTests(TestCase):
    """Testcase for vote model."""

    def setUp(self):
        """Create a test user for testing."""
        test_user = User.objects.create_user("Testaccount", "Test@gmail.com")
        test_user.set_password("Ilovecoding")
        test_user.save()

    def test_not_login_user_vote(self):
        """Redirect a user to login page if a user is not authenticated."""
        lct = timezone.localtime()
        question = Question.objects.create(question_text="1", pub_date=lct)
        url = reverse('polls:vote', args=(question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_authenticated_user_vote(self):
        """Test that authenticated user can vote a question."""
        lct = timezone.localtime()
        self.client.login(username="Testaccount", password="Ilovecoding")
        question = Question.objects.create(question_text="2", pub_date=lct)
        url = reverse('polls:vote', args=(question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class QuestionIndexViewTests(TestCase):
    """Testcase for Index view."""

    def test_no_questions(self):
        """If no questions exist, an appropriate message is displayed."""
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """Questions within past date are displayed on theindex page."""
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_future_question(self):
        """Questions with future date aren't displayed on the index page."""
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """Only past questions are displayed."""
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_two_past_questions(self):
        """The questions index page may display multiple questions."""
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question2, question1],
        )


class QuestionDetailViewTests(TestCase):
    """Testcase for Detail view test."""

    client = Client()

    def setUp(self):
        """Create a test user for testing."""
        self.test_user = User.objects.create_user("Python", "Test@gmail.com")
        self.test_user.set_password("Ilovecoding")
        self.test_user.save()

    def test_Login(self):
        """Returns a 200 status respond."""
        self.client.login(username='Python', password='Ilovecoding')
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)

    def test_question(self):
        """Check if a question is contained a question text or not."""
        question = create_question(question_text="1", days=1)
        url = reverse("polls:details", args=(question.id,))
        response = self.client.get(url)
        self.assertContains(response, question.question_text)
