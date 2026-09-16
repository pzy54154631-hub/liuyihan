+++
title = "会计分录与报表：让数字彼此对得上"
date = "2026-09-16"
tag = "LaTeX 学习手记"
summary = "用一组模拟交易串起借贷分录、利润、资产负债和现金流，练习报表间的勾稽关系。"
authors = ["Ziyu Peng", "刘毅涵"]
series = "latex"
order = 12
stage = "第四阶段 · 带进经管课堂"
+++

会计表格的难点常常不在横线，而在同一个金额进入不同报表以后是否仍然说得通。本篇从一组模拟交易出发，先写借贷分录，再整理利润、期末资产负债和现金流。这样做出来的文档既能阅读，也能检查。

案例为自设的服务工作室，期初各项余额为零，金额统一为元；不考虑税费，期间内没有利润分配，设备当期折旧直接给定为 100 元。耗材购入时计为资产，实际耗用时计为费用。这是一份用于说明基本关系的简化教学报表，不是特定会计准则下的完整披露模板。

## 借方、贷方不是“收入、支出”的别名

复式记账要求每一笔分录的借方金额合计等于贷方金额合计。资产增加通常记借方，负债和权益增加通常记贷方；收入增加通常记贷方，费用增加通常记借方。资产的抵减账户等有自身的方向，不能把“所有借方都增加资产”当作通用规则。基本恒等式是：

$$
\text{资产}=\text{负债}+\text{所有者权益}.
$$

这些关系可以结合 [OpenStax 的会计等式说明](https://openstax.org/books/principles-financial-accounting/pages/3-1-describe-principles-assumptions-and-concepts-of-accounting-and-their-relationship-to-financial-statements) 阅读。排版时把科目与借贷金额分列，比把整条分录写成一段文字更容易检查。

## 用八件事搭起一组报表

| 事项 | 本期发生的交易或调整 |
| --- | --- |
| 1 | 收到所有者投入现金 10,000 元。 |
| 2 | 支付现金 3,000 元购入设备。 |
| 3 | 支付现金 600 元购入耗材。 |
| 4 | 赊购耗材 500 元，款项尚未支付。 |
| 5 | 完成服务，确认收入 2,400 元；收到 1,800 元，另有 600 元待收。 |
| 6 | 支付本期租金 500 元。 |
| 7 | 期末确认本期耗用耗材 200 元。 |
| 8 | 期末确认设备折旧 100 元。 |

第五笔是复合分录：借记银行存款 1800、应收账款 600，贷记服务收入 2400。确认收入并不要求已经把全部款项收到手；本例假定服务已经完成、收入在本期确认。分录中的时间判断要先正确，表格才能反映正确的期间。

第三、四笔购入耗材合计 1100 元，实际耗用 200 元，所以期末还剩 900 元。把购入耗材的全部金额直接写成本期费用，会让利润和期末资产一起出错。

## 三张表怎样互相核对

本期利润为 $2400-500-200-100=1600$ 元。期末权益由投入资本 10000 元与本期留存利润 1600 元构成，合计 11600 元。这里省略税费只是题目假设，并不是现实企业都可以省略税费。

期末银行存款为 $10000-3000-600+1800-500=7700$ 元；加上应收账款 600、耗材 900 和设备净额 $3000-100=2900$，资产总额为 12100 元。另一侧，应付账款 500 元加权益 11600 元，也得到 12100 元。累计折旧是设备资产的抵减项，不能为了凑平衡把它列作负债。

现金流按本例的活动性质分组：经营活动净流入 $1800-600-500=700$ 元，投资活动净流出 3000 元，筹资活动净流入 10000 元，合计增加 7700 元，与期末银行存款一致。赊购耗材没有发生本期现金支付，因此不能又在现金流里扣一遍。

利润是 1600 元，经营现金流却是 700 元，并不矛盾。收入中有 600 元尚未收回，耗材仍占用资源，折旧又不是本期现金支出。用间接核对方式表示，就是 $1600+100-600-900+500=700$。了解报表之间的连接，可以阅读 [OpenStax 的财务报表关系章节](https://openstax.org/books/principles-financial-accounting/pages/2-1-describe-the-income-statement-statement-of-owners-equity-balance-sheet-and-statement-of-cash-flows-and-how-they-interrelate)。

## 排版时保留“可核对性”

分录多了会跨页，所以完整示例使用 `longtable`，重复显示列标题。这个环境不要再套入 `table` 浮动体；较短的报表则用普通 `tabular` 与 `booktabs`。金额列右对齐，单位写在表头或图注，不要每格都重复写“元”。宏包细节可查 [longtable 文档入口](https://ctan.org/pkg/longtable)。

表名还应区分期间：利润表和现金流描述“本期发生了什么”，资产负债表描述“期末还拥有什么、承担什么”。正式作业中，把具体期间和期末日期写在表名附近，能避免两种口径混在一起。

## 可编译示例

[下载本章完整示例](/liuyihan/assets/tutorial/examples/latex-12.tex)。使用 XeLaTeX 编译两遍。文件包括全部分录和三张简化报表，不依赖外部账簿。

```latex
% !TeX program = xelatex
% 自设会计教学案例；金额单位为元，不对应任何企业。
\documentclass[UTF8,a4paper,fontset=fandol]{ctexart}
\usepackage[margin=2.2cm]{geometry}
\usepackage{amsmath,amssymb,booktabs,longtable,array}
\usepackage[hidelinks]{hyperref}
\title{会计分录与报表：让同一组数字相互勾稽}
\author{\href{https://github.com/pzy54154631-hub}{\textit{Ziyu Peng}}, University of Colorado Boulder
  \\[0.35em]
  \href{https://pzy54154631-hub.github.io/liuyihan/}{刘毅涵}，暨南大学经济学院}
\date{}
\begin{document}
\maketitle
假设一家模拟服务工作室期初余额全部为零。下面记录一个教学期间的交易，
不考虑税费，期末无分红；设备本期折旧给定为 100。
耗材购入时先确认为资产，本期耗用部分才转为费用。
所有数值均为自设，报表是为解释勾稽关系而简化的教学版。

\section{分录：每笔借贷相等}
\begin{longtable}{@{}p{1cm}p{4.9cm}rr@{}}
\caption{模拟交易分录（单位：元）}\label{tab:entries}\\
\toprule
事项 & 科目 & 借方 & 贷方\\
\midrule
\endfirsthead
\toprule
事项 & 科目 & 借方 & 贷方\\
\midrule
\endhead
\midrule
\multicolumn{4}{r}{续下页}\\
\endfoot
\bottomrule
\endlastfoot
1 & 银行存款 & 10000 & \\
  & \quad 投入资本 & & 10000\\
\addlinespace
2 & 设备 & 3000 & \\
  & \quad 银行存款 & & 3000\\
\addlinespace
3 & 耗材 & 600 & \\
  & \quad 银行存款 & & 600\\
\addlinespace
4 & 耗材 & 500 & \\
  & \quad 应付账款 & & 500\\
\addlinespace
5 & 银行存款 & 1800 & \\
  & 应收账款 & 600 & \\
  & \quad 服务收入 & & 2400\\
\addlinespace
6 & 租金费用 & 500 & \\
  & \quad 银行存款 & & 500\\
\addlinespace
7 & 耗材费用 & 200 & \\
  & \quad 耗材 & & 200\\
\addlinespace
8 & 折旧费用 & 100 & \\
  & \quad 累计折旧 & & 100\\
\end{longtable}

\section{本期利润与期末权益}
\begin{center}
\begin{tabular}{lr}
\toprule
利润表项目 & 金额（元）\\
\midrule
服务收入 & 2400\\
减：租金费用 & 500\\
减：耗材费用 & 200\\
减：折旧费用 & 100\\
\midrule
本期利润 & 1600\\
\bottomrule
\end{tabular}
\end{center}
在本例无税费的设定下，本期利润为 1600。期末权益为
$0+10000+1600-0=11600$，依次对应期初权益、投入、本期利润和分配。

\section{期末资产负债表}
\begin{center}
\begin{tabular}{lr}
\toprule
资产项目 & 金额（元）\\
\midrule
银行存款 & 7700\\
应收账款 & 600\\
耗材 & 900\\
设备原值 & 3000\\
减：累计折旧 & 100\\
\midrule
资产总计 & 12100\\
\midrule
负债和权益项目 & 金额（元）\\
\midrule
应付账款 & 500\\
投入资本 & 10000\\
本期形成的留存利润 & 1600\\
\midrule
负债和权益合计 & 12100\\
\bottomrule
\end{tabular}
\end{center}
核对 $12100=500+11600$。累计折旧抵减设备账面价值，并非负债。

\clearpage
\section{本期现金流量汇总}
\begin{center}
\begin{tabular}{lr}
\toprule
项目 & 金额（元）\\
\midrule
经营：收到服务款 & 1800\\
经营：购入耗材支付 & -600\\
经营：支付租金 & -500\\
经营活动现金流量净额 & 700\\
\midrule
投资：购买设备 & -3000\\
筹资：收到投入资本 & 10000\\
\midrule
现金净增加额 & 7700\\
期初现金余额 & 0\\
期末现金余额 & 7700\\
\bottomrule
\end{tabular}
\end{center}
赊购耗材 500 不产生本期现金收付。折旧 100 也不直接产生现金收付。
本例银行存款即现金流量表中的现金，未另设现金等价物。
以间接思路核对经营现金流：
\[
1600+100-600-900+500=700.
\]
各项依次为利润、折旧、应收增加、耗材增加和应付增加。
\end{document}
```

## 小练习：收回应收款以后

在期末前再收回 300 元应收账款，暂不增加任何其他交易。先补写“借：银行存款 300；贷：应收账款 300”，再更新报表。利润仍为 1600 元，现金变为 8000 元，应收账款降到 300 元，资产总额仍为 12100 元，经营现金流增至 1000 元。如果你把这次收款再次写成收入，利润就被重复确认了。
