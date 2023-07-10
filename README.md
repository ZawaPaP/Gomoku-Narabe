# TicTacToe Game

## 1. Introduction
### 1.1 Purpose
The purpose of this document is to define the requirements for the development. It outlines the goals, features, and constraints of the product.

### 1.2 Scope
The scope of this project includes the development of TicTacToe Game in console considered the scalability, code readability and usability for practice of software architecture building.
Success criteria is completing a working TicTacToe Game and passing self-test cases.

## 2. Product Features
TicTacToe Game

## 3. Functional Requirements
### 3.1 ver 1
* Display game board
* Display game status
* Display player's turn
* Accept console input
* Accept game reset / exit
### 3.2 ver 2
* Player vs CPU
* Select the player turn (if vs CPU)

## 4. Non Functional Requirements
NA

--------
## Review

* better to separate get_move and set_move because set_move belong to Game
    *  純粋関数 とはsame input / same outputかつ 関数の中身が変わらない関数のこと
    * 純粋関数以外はできるだけ避けるべき, make_moveはboardのstate変更をしてしまっているため、純粋関数ではない
    * set_moveはboard.set_moveにすれば、純粋関数になる
    * 正確にはraise ErrorなどもOutputだが、それは仕方がない > boolでの判断など入れれば純粋関数になる

07 Jul review
* マジックナンバーは使わない
* 関数はBehaviorを表す

03 Jul review
* 再帰について
    * 再帰を使うケース > 親でも子でも帰ってくるデータが同じように見えるケース
        * ツリーやグラフ
    * 再帰呼び出しはコードを追いづらい＆エラーになりやすい(わかりづらい)ため、できるだけ避ける
* Try - except の改善
* Debug: Already marked のときターンが変わる
* make_actionとplay内でのコード重複
* Actionはゲームから取る必要がない (resetはゲームのリセットなのでゲーム内で処理されるべき)
* Handlerという名前をつけるなら、Handler内で処理を完結させ、Returnしないのが基本


--------

Memo:  
*Enumとは*
Enum（列挙型）は、プログラミングにおいて特定の値の集合を表現するためのデータ型です。Enumは、あるデータが特定の値の中から選ばれることを保証するために使用されます。  

*IOとIO Controllerを分ける意味は？*
IOはデータの入出力や外部リソースの操作に関する責任を持ち、IOコントローラモジュールはデータの制御やビジネスロジックに関する責任を持ちます。これにより、コードの再利用性やテスト容易性が向上し、各モジュールの責務が明確になります。  

*＠staticmethod*
静的メソッドは、クラスの中で共有のユーティリティ関数や、インスタンスに依存しない処理を実装する場合に便利です。インスタンスの状態にアクセスする必要がない場合や、外部の依存関係を持たない単純な処理を実行する場合に使用されます。

*try-exceptについて*
予期できるエラーは例外処理をすべき。予期できないエラーは異なる処理をしてexitすべき。例外処理は低い階層ではなく、controllerなどの層で制御を行う。例外発生した際の処理をまとめて書きやすい