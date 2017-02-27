#coding=utf8
import json

class MonthPayInfo(object):
    month_idx = None
    lave_bj = None
    pay_total = None
    pay_bj = None
    pay_bx = None

    def as_dict(self):
        return {
            "月份": self.month_idx,
            "剩余本金": int(self.lave_bj),
            "支付本金": int(self.pay_bj),
            "支付本息": int(self.pay_bx),
            "支付总和": int(self.pay_total)
        }

    def __str__(self):
        return json.dumps(self.as_dict(), ensure_ascii=False, indent=4)


class DaiKuan(object):

    def __init__(self, total, lilv, years=0, months=0):
        self.total = float(total)
        self.yuelilv = lilv / 12
        self.months = years * 12 + months

    def debx_future_pays(self):
        """等额本息"""
        bj = self.total
        yll = self.yuelilv
        month_to_pay = bj * yll * ((1 + yll) ** 192) / ((1 + yll) ** 192 - 1)
        rst = []
        for i in range(self.months):
            mp = MonthPayInfo()
            mp.month_idx = i + 1
            mp.pay_total = month_to_pay
            mp.pay_bx = bj * self.yuelilv
            mp.pay_bj = mp.pay_total - mp.pay_bx
            rst.append(mp)
        return rst

    def debj_future_pays(self):
        """等额本金"""
        benjin = self.total
        yuelilv = self.yuelilv
        yuebenjin = benjin / self.months
        rst = []
        for month_idx in range(self.months):
            mp = MonthPayInfo()
            mp.month_idx = month_idx + 1
            mp.pay_bx = benjin * yuelilv
            mp.pay_bj = yuebenjin
            mp.pay_total = mp.pay_bj + mp.pay_bx
            benjin -= yuebenjin
            mp.lave_bj = benjin
            rst.append(mp)
        return rst


if __name__ == "__main__":
    d = DaiKuan(1200000, 0.0325, years=16)
    rst = d.debj_future_pays()
    for i in range(len(rst) - 2):
        print int(rst[i].pay_bx), int(rst[i+1].pay_bx), '%.2f' % (rst[i+1].pay_bx - rst[i].pay_bx)