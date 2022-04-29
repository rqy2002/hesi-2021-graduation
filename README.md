# 荷思 2021 毕业专刊

这是 2022 年编撰的《荷思》杂志 2021 毕业专刊的源代码。

## 如何添加文章

每篇文章放在 `papers` 目录的一个单独的子目录中，例如 `papers/YourPaper`。目录应直接包含下列文件：

* 主文件 `YourPaper.tex`，文件名应与目录名相同。
* 命令定义文件 `commands.tex`，作者自己定义的命令等写在其中。
* 参考文献文件 `YourPaper.bib`。我们用 `biblatex` 处理参考文献。

较长的文章应该分成多个文件，然后在主文件中引用。

### 主文件示例

```latex
\documentclass[twoside]{article}

\input{../common/preamble}
\input{../common/preamble-zh}  % 只有中文文章需要这一行
\input{commands}

\addbibresource{YourPaper.bib}

\begin{document}

\title{标题}
\author{作者\footnote{作者信息}}
\headertitle{放在页眉的文章标题}  % 若与标题相同，可省略

\begin{abstract}
    摘要 ...
\end{abstract}

正文 ...

\printbibliography

\end{document}
```

## 如何编译

要编译整本《荷思》，需安装 Python 3，并运行以下命令行：

``` bash
pip install pypdf2
python build.py
```

如果要取得电子版（具有目录和链接），需安装 Python 3 和 pdftk（目前仅支持 Linux 编译），
并运行以下命令：

``` bash
python build_ebook.py
```

你也可以从 Releases 界面下载《荷思》或其电子版。

如果要单独编译一篇文章，进入该文章的文件夹，并运行：

``` bash
latexmk -pdf -xelatex YourPaper.tex
```

## LaTeX 排版规范

作者在提交代码时，应确保 LaTeX 代码满足以下要求（虽然这里面的很多代码并不满足这些要求）。

### 代码风格

* 代码中不能有过长的行。每行不可超过 80 个字符。

* 环境的内容（不含开始和结束）使用 4 个空格缩进，并且这些内容必须独占一行或多行。在任何合适的情况下，环境的前后用空行隔开。例如
    ```latex
    \begin{theorem}
        This is a theorem.
    \end{theorem}

    \begin{proof}
        This is a proof.
    \end{proof}
    ```
    对于跨多行的 `\[ \]` 、 `{ }` 或 `[ ]` 等等而言，以上也适用。它们包含的部分也需要缩进、独占一行或多行。例如：
    ```latex
    错误示例：
    \[A=\begin{pmatrix}a_{11}&a_{12}\\a_{21}&a_{22}\end{pmatrix}.\]

    正确示例：
    \[
        A = \begin{pmatrix}
            a_{11} & a_{12} \\
            a_{21} & a_{22}
        \end{pmatrix} .
    \]
    ```

* `\[ \]` 数学公式要么独占一行，要么跨多行，且后一种情况下，其内容需要缩进。

* 不要省略命令参数的大括号。例如 `\mathbb{Z}` ， `\frac{1}{2}` 。一个例外是公式中 `^` 和 `_` 的参数，例如 `x^2` 。

* 数学公式中，应多加空格，以保证可读性。下列情况下必须加空格。

    * 在关系和二元运算符两侧，例如 `1 + 1 = 2` ， `A \oplus B \simeq C` 。
    * 在逗号、分号之后。例如 `f(x, y; z)` 。
    * 在 `\[ \]` 内侧。例如 `\[ f(x) < f(x + 1) \]` 。
    * 在 `\{ \}` 和 `\left(` 、 `\bigr\}` 等的两侧。

* 在任何 `\\` 之后换行。若带有可选参数，例如 `\\[5pt]` ，则在可选参数后换行。

* 尽量使用 `\newcommand` 或 `\renewcommand` ，而不要使用 `\def` ，除非你知道为什么必须用 `\def` 。

### 文字排版

* 英文标点符号 `, . : ; ? !` 之前不加空格，之后加空格，除非它后面紧接一个右括号或下引号。

* 中文与西文之间应有 1 个空格。虽然 `xeCJK` 宏包会自动保证这一点，但不一定能处理所有特殊情况。因此，应该在源码中保持这个习惯。

* 除非在数学公式或表格中，否则不要使用 `\\` 进行换行。

* 注意区分 `-` 、 `--` 、 `---` 。
    * `-` 是连字符 (-)，用于单词中，例如 `well-known` ，或连接同一姓氏的不同部分，例如 `Levi-Civita` 。
    * `--` 是短横线 (&ndash;)，用于连接两个人名，例如 `Newton--Leibniz` ，或连接两个数字，例如 `1--10` 。
    * `---` 是长横线 (&mdash;)，用作破折号。中文破折号由两个长横线构成，即 `------` 。
    * 以上三者都不能作为减号或负号 (&minus;)。

* 单引号是 `` ` ' `` ，而不是 `' '` 。双引号是 ``` `` '' ``` ，而不是 `" "`。

* 在不是句号的点号之后加 `\ ` ，例如 `i.e.\ ` 。这是为了防止被看作一句话的结束，导致增加间距。对 `!` 和 `?` 等也一样。一个例外是，当点号之前的最后一个字母是大写字母时，不需要这么做。例如， `I. Newton` 会给出正确的间距。

* 每个数学公式都是句子的成分，应确保语法正确。公式中的标点符号不可省略。例如：
    ```latex
    The fact that
    \[ 1 + 1 = 2 \]
    implies that
    \[ 1 + 1 < 3. \]
    ```

* 使用 `\newtheorem` 创建定理环境，使用 `theorem` 计数器编号。如需更改已经在导言中定义的定理环境，导言提供了 `\renewtheorem` 命令供作者使用。

* 章节标题中，若有数学公式，需要用 `\texorpdfstring` 产生正确的 PDF 书签。例如：
    ```latex
    \section{\texorpdfstring{$C^*$}{C*} 代数}
    ```

### 数学公式

* 使用 `\[ ... \]` ，而不要使用 `$$ ... $$` 。后者会导致一些排版问题。例如，它会产生不正确的段落间距；它不支持 `\qedhere` 。

* 注意区分 `:` 和 `\colon` 。前者表示比例、子群的指标等，例如
`[G : H]` 。后者表示映射，例如 `f \colon X \to Y` 。它们的区别是间距不同。

* 注意区分 `|` 和 `\mid` 。前者两侧没有间距，而后者有。例如：
    ```latex
    \{ x \in \mathbb{R} \mid |x| < 1 \}
    ```
    当 `|` 表示绝对值时，也要注意间距。例如 `|\sin x|` 会在前一个 `|` 和 `sin` 之间多出一个空白。解决的办法是：
    ```latex
    \left| \sin x \right| 或者 \mathopen{|} \sin x \mathclose{|}
    ```

* 使用 `\operatorname{...}` 或 `\operatornamewithlimits{...}` 表示多个字母组成的运算符。二者的区别是，在居中公式里，后者会把上下标写在符号的正上方和正下方。例如：
    ```latex
    \operatorname{Hom}(X, Y) \simeq \operatornamewithlimits{colim}_{i \in I} Z_i
    ```
    
    对于那些不是运算符的由多个字母组成的记号，使用 `\mathrm{...}` 。例如：
    ```latex
    f = f_{\mathrm{even}} + f_{\mathrm{odd}}
    ```

* 如果一个逗号分隔了两个较长的部分，那么逗号之后需要插入空格 `\ ` 。例如：
    ```latex
    \{ x \in \mathbb{R} \mid x > 0,\ x < 1 \}.
    ```
    这样得到的空格与 `$x > 0$, $x < 1$` 是相同的。

* 使用 `tikzcd` 画交换图。虽然 `\xymatrix` 有同样的功能，但它不够灵活，样式难以更改，并且带钩的箭头 (&rarrhk;) 很不好看。

* 不要使用任何提供字体和符号的宏包。我们使用 `unicode-math` ，所有的公式都使用 Unicode 编码。原因如下：第一，在 TeX 中，提供字体和符号的宏包非常容易导致问题（后果是编译不过）。这是 TeX 最令人头疼的问题之一，而 XeTeX 通过支持 Unicode 解决了这个问题。第二，任何现代的电子文档都应该使用 Unicode。第三，Unicode 包含了几乎任何你想要的符号。如果一个符号未被 Unicode 包含，你大概也不该在文章里使用它。

## 导言提供的功能

### 定理环境

* 导言提供的定理环境有 `theorem`, `corollary`, `definition`, `example`, `lemma`, `proposition`, `remark`。定理计数器是 `theorem`。

* 如需重新定义定理环境，导言提供了 `\renewtheorem` 命令。

* 导言 `preamble-zh.tex` 提供了三种定理样式：`cjk-theorem`, `cjk-definition`, `cjk-remark`。新样式与原来的区别是，原来的样式中使用斜体的部分，在新的样式中使用楷体，但西文字符不使用斜体，因为在中文文档中，这样是最合适的。作者可以通过 `\theoremstyle` 来使用它们。

* `\thmqedhere` 命令，用来给没有证明且以公式结束的定理添加证毕符号。此时 `\qed` 和 `\qedhere` 都不起作用。
