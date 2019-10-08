from main import models


class BaseModel(models.Model):
    __abstract__ = True  # 声明当前类是抽象类，被继承调用不被创建
    id = models.Column(models.Integer, primary_key=True, autoincrement=True)

    def save(self):
        db = models.session()
        db.add(self)
        db.commit()

    def delete(self):
        db = models.session()
        db.delete(self)
        db.commit()


# 定义表:课程表
class Curriculum(BaseModel):
    __tablename__ = "curriculum"
    c_id = models.Column(models.String(32))
    c_name = models.Column(models.String(32))
    c_time = models.Column(models.Date)


class User(BaseModel):
    __tablename__ = "user"
    user_name = models.Column(models.String(32))
    password = models.Column(models.String(32))
    email = models.Column(models.String(32))


class Leave(BaseModel):
    __tablename__="leave"
    request_id=models.Column(models.Integer)#请假人id
    request_name=models.Column(models.String(32))#请假人姓名
    request_type=models.Column(models.String(32))#请假类型
    request_start_time=models.Column(models.String(32))#请假开始时间
    request_end_time=models.Column(models.String(32))#请假结束时间
    request_description=models.Column(models.Text)#请假原因
    request__phone=models.Column(models.String(32)) #联系方式
    request_static=models.Column(models.String(32)) #佳田状态 批准或者不批准


class Picture(BaseModel):
    picture=models.Column(models.String(64))