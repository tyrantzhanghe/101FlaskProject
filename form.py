import wtforms
from flask_wtf import FlaskForm
from wtforms import validators
from wtforms import ValidationError

#自定义错误类型
def keywords_valid(form,field):
    data=field.data
    keywords=["admin","管理员","superuser"]
    if data in keywords:
        raise ValidationError("关键词错误")
class Task(FlaskForm):
    name=wtforms.StringField(
        render_kw={
            "class":"form-control",
            "placeholder":"任务名称"
        },
        validators=[
            validators.DataRequired("姓名不可以为空"),
            validators.length(max=16,min=6)
        ]
    )
    description = wtforms.TextField(
        render_kw={
            "class":"form-control",
            "placeholder":"邮箱测试"
        },
        validators=[
            validators.Email("请输入正确的邮箱")
        ]
    )
    time = wtforms.DateField(
        render_kw={
            "class":"form-control",
            "placeholder":"关键词错误测试"
        }
    )
    public = wtforms.StringField(
        render_kw={
            "class":"form-control",
            "placeholder":"任务发布人"
        }
    )