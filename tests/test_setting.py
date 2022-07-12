from libs.setting import Setting
import logging
class Test_Setting:

    def test_setting(self,Tk,TestAPI):
        Owner = "TEST"
        s = Setting(root=Tk,file="None",mode="TEST")
        s.EditBox1.insert(0, TestAPI)
        s.EditBox2.insert(0, Owner)
        logging.info(s.EditBox1.get())
        logging.info(s.EditBox2.get())
        assert s.EditBox1.get() == TestAPI
        assert s.EditBox2.get() == Owner

    def test_api_error_check(self,Tk):
        s = Setting(root=Tk,file="None",mode="TEST")
        s.EditBox1.insert(0, "API")
        msg = s.button_action()
        logging.info(msg)
        assert msg == "API Error"

    def test_user_error_check(self,Tk,TestAPI):
        s = Setting(root=Tk,file="None",mode="TEST")
        s.EditBox1.insert(0, TestAPI)
        s.EditBox2.insert(0,"")
        msg = s.button_action()
        logging.info(msg)
        assert msg == "User Error"