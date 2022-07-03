from libs.setting import Setting

class Test_Setting:
    def test_setting(self,Tk,TestAPI):
        Owner = "TEST"
        s = Setting(root=Tk,file="None",mode="TEST")
        s.EditBox1.insert(0, TestAPI)
        s.EditBox2.insert(0, Owner)
        assert s.EditBox1.get() == TestAPI
        assert s.EditBox2.get() == Owner

    def test_api_error_check(self,Tk):
        s = Setting(root=Tk,file="None",mode="TEST")
        s.EditBox1.insert(0, "API")
        msg = s.button_action()
        assert msg == "API Error"

    def test_user_error_check(self,Tk,TestAPI):
        s = Setting(root=Tk,file="None",mode="TEST")
        s.EditBox1.insert(0, TestAPI)
        s.EditBox2.insert(0,"")
        msg = s.button_action()
        assert msg == "User Error"