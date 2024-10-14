from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .models import Question


class QuestionIndexViewTests(TestCase):
    def setUp(self):
        self.question1 = Question.objects.create(
            question="What's new?",
            pub_date=timezone.now(),
        )
        self.question2 = Question.objects.create(
            question="What's your favorite color?", pub_date=timezone.now()
        )

    def test_index_view_status_code(self):
        """
        Test that the index view returns a 200 status code.
        """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)

    def test_index_view_template_used(self):
        """
        Test that the index view uses the correct template.
        """
        response = self.client.get(reverse("polls:index"))
        self.assertTemplateUsed(response, "polls/index.html")

    def test_index_view_context_with_questions(self):
        """
        Test that the context contains the correct questions.
        """
        response = self.client.get(reverse("polls:index"))
        self.assertIn(self.question1, response.context["latest_question_list"])
        self.assertIn(self.question2, response.context["latest_question_list"])

    def test_index_view_no_questions(self):
        """
        Test the index view with no questions.
        """
        Question.objects.all().delete()
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls available.")

    def test_index_view_limit_questions(self):
        """
        Test that the index view only shows the latest 5 questions.
        """
        for i in range(6):
            Question.objects.create(question=f"Question {i}", pub_date=timezone.now())
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(len(response.context["latest_question_list"]), 5)
