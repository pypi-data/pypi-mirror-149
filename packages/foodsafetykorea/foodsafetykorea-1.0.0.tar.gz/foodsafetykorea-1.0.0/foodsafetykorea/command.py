import argparse

from tkinter import messagebox
from tkinter.ttk import Combobox
from tkinter import Tk, Button, Label, StringVar

from . import (
    select_school_meals,
    select_school_week_meals_detail,
    select_week_year_list,
    select_school_meals_info,
    to_dict,
)

parser = argparse.ArgumentParser()
parser.add_argument('school')
parser.add_argument('--region', default=None)

arguments = parser.parse_args()

def main(school, region):
    def select():
        nonlocal school, region
        schools = select_school_meals(school, region)
        if not schools:
            raise ValueError('검색된 학교가 없습니다.')
        school_names = [f'{school.ara} {school.schl_nm}' for school in schools]

        root = Tk()

        def purge():
            root.quit()

        var = StringVar(root, '학교 선택')

        selections = Combobox(root, values=school_names, textvariable=var)
        purge_button = Button(root, text='확인', command=purge)

        selections.pack(fill='x')
        purge_button.pack(fill='x')

        root.mainloop()
        try:
            return list(
                filter(
                    lambda value: f'{value.ara} {value.schl_nm}' == var.get(), schools,
                )
            )[0]
        except IndexError:
            raise TypeError('심각한 오류가 발생 했습니다.')

    map = select()
    selected = select_school_meals_info(map, region)
    select_week_year_list(selected)
    result = select_school_week_meals_detail(selected)
    lunch = to_dict(result)

    def check_lunch():
        nonlocal lunch
        root = Tk()
        root.title('급식')
        root.resizable(False, False)

        def show(text):
            return messagebox.showinfo('급식', text)

        __monday__ = Button(root, text='월', command=lambda: show(lunch['월']))
        __thuesday__ = Button(root, text='화', command=lambda: show(lunch['화']))
        __wednesday__ = Button(root, text='수', command=lambda: show(lunch['수']))
        __thursday__ = Button(root, text='목', command=lambda: show(lunch['목']))
        __friday__ = Button(root, text='금', command=lambda: show(lunch['금']))
        __saturday__ = Button(root, text='토', command=lambda: show(lunch['토']))
        __sunday__ = Button(root, text='일', command=lambda: show(lunch['일']))

        local = locals()

        for button in local:
            if isinstance(local[button], Button):
                local[button].config(padx=10)
                local[button].update()
                local[button].pack(side='left', fill='y')
            else:
                continue

        allergy = Label(root, text='알레르기 유발식품: ①-난류 ②-우유 ③-메밀 ④-땅콩 ⑤-대두\n⑥-밀 ⑦-고등어 ⑧-게 ⑨-새우 ⑩-돼지고기 ⑪-복숭아 ⑫-토마토\n⑬-아황산염')
        allergy.pack()

        def purge():
            nonlocal root
            root.destroy()
            return None

        root.protocol('WM_DELETE_WINDOW', purge)
        root.mainloop()

    check_lunch()

if __name__ == '__main__':
    main(arguments.school, arguments.region)