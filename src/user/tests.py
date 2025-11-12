from django.test import TestCase
from user.models import User
from boards.models import Board

class FilterBoardsTest(TestCase):
    def setUp(self):
        
        self.client_user = User.objects.create(name="Client", role="client", email="client@example.com")
        self.admin_user = User.objects.create(name="Admin", role="admin", email="admin@example.com")
        self.super_admin = User.objects.create(name="Super Admin", role="super_admin", email="superadmin@example.com")

        
        self.board1 = Board.objects.create(name="Board 1", location="NY", width=200, height=400, admin=self.admin_user)
        self.board2 = Board.objects.create(name="Board 2", location="LA", width=100, height=100, admin=self.admin_user)
        self.board3 = Board.objects.create(name="Board 3", location="NY", width=400,height=400,admin=self.admin_user)

    def test_client_filter_boards(self):
        print("\n[Client] No filters:", self.client_user.filter_boards())
        print("[Client] Location='NY':", self.client_user.filter_boards(location="NY"))
        print("[Client] Size='medium':", self.client_user.filter_boards(size="medium"))
        print("[Client] Location='NY', Size='medium':", self.client_user.filter_boards(location="NY", size="medium"))

    def test_admin_filter_boards(self):
        print("\n[Admin] No filters:", self.admin_user.filter_boards())
        print("[Admin] Location='Tokyo':", self.admin_user.filter_boards(location="Tokyo"))
        print("[Admin] Size='medium':", self.admin_user.filter_boards(size="medium"))
        print("[Admin] Location='NY', Size='medium':", self.admin_user.filter_boards(location="NY", size="medium"))

    def test_superadmin_filter_boards(self):
        print("\n[Superadmin] No filters:", self.super_admin.filter_boards())
        print("[Superadmin] Location='NY':", self.super_admin.filter_boards(location="NY"))
        print("[Superadmin] Size='large':", self.super_admin.filter_boards(size="large"))
        print("[Superadmin] Location='Tokyo', Size='medium':", self.super_admin.filter_boards(location="Tokyo", size="medium"))