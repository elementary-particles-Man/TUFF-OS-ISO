**TUFF-OS Isolationモード 復帰手順 詳細説明**

Isolationモードは、TUFF-OSの最終防衛機構です。  
一度発動すると、**通常のログインやコマンド操作は完全に拒否**され、システムは物理層・ネットワーク層ともに遮断状態になります。  
復帰は**極めて厳格に制限**されており、誤操作や攻撃者による解除を防止する設計です。

### 復帰可能な条件（唯一の正規経路）

復帰できるのは**以下の条件をすべて満たした場合のみ**です：

1. 管理者権限を持つユーザー（rootまたはadmin権限付与済み）
2. 正しいRecovery PIN（12桁以上、インストール時に生成・暗号保存されたもの）
3. システムが物理的に安全な状態（改ざんがないこと）

**一般ユーザー**、**PINを知らない人**、**PINが漏洩した攻撃者**は**絶対に復帰できません**。

### 復帰手順（ステップ・バイ・ステップ）

#### Step 1: 現在の状態を確認する（任意だが強く推奨）

- ログイン不能画面に「System Isolated」または「TUFF-OS Isolation Mode Active」と表示されていることを確認。
- 可能であれば別の端末からwitness.logを確認（USB経由など）  
  → 「Isolation mode triggered by ...」という最終記録があるはず

#### Step 2: Recovery PINを準備する

- インストール時に生成された**TUFFkey.json**（USBメモリ推奨）を開く  
  → JSON内に `"recovery_pin": "XXXXXXXXXXXX"` の項目がある
- PINを入力ミスしないよう、**紙にメモ**するか安全な場所に控える

**PIN紛失時の唯一の手段**  
→ 再インストール（全データ消去）しかありません。  
→ バックアップから復旧する場合は、**外部ストレージからrestore**が必要

#### Step 3: 復帰コマンドを実行

**CUIモード**（VGAテキスト画面）または**SSH/シリアルコンソール**から以下のコマンドを実行：

```bash
tuffutl sys isolation recover --pin XXXXXXXXXXXX
```

- `--pin` の後にスペースを空けて12桁のPINを入力
- 正しいPINの場合、即座に処理開始（所要時間：約2〜5秒）

**成功時の画面例**
```
Recovery PIN accepted.
Zeroizing remaining session data... OK
Clearing Isolation Persistent flag... OK
Reinitializing I/O Gatekeeper... OK
ネットワーク防衛ルール restored... OK
System recovered from Isolation mode.
Please login again.
```

**失敗時の主なエラー例**

| エラーメッセージ | 原因 | 対処 |
|------------------|------|------|
| Invalid Recovery PIN | PIN誤り | 正しいPINを再入力（3回失敗で一時ロック） |
| Isolation not active | すでに解除済み | 通常ログイン可能 |
| Consensus Failure | 3N不一致（改ざん疑い） | ディスク交換後 `fsck --repair` |
| Hardware ID mismatch | ディスク持ち出し・改ざん | 再インストール必須 |

#### Step 4: 復帰後の必須確認・対応

1. **即時ログイン**  
   ```bash
   tuffutl sys login <your_id> --password <your_pw>
   ```

2. **状態再確認**  
   ```bash
   tuffutl sys status --detail
   ```
   → Isolation: Inactive になっていることを確認

3. **証跡確認**  
   ```bash
   tuffutl log tail --lines 50
   ```
   → 「Isolation recovered at ...」の記録を確認（PQC署名付き）

4. **再発防止策**（強く推奨）
   - トリガー原因の特定（witness.logを精査）
   - パスワード変更（`tuffutl user password`）
   - ネットワークポリシー見直し（`tuffutl nw blacklist` / `aiserverlist`）
   - 物理アクセス制限の強化

### 重要ルールまとめ

- **PINは絶対に漏洩させない**  
  → 紛失時は全データ再構築（バックアップ必須）
- **復帰後もすぐには信用しない**  
  → 復帰直後に `fs fsck` と `nw status` を実行し、異常がないか確認
- **訓練推奨**  
  → 定期的に `tuffutl sys isolation trigger` で訓練 → `recover` で解除を練習

### 運用上のTips

- **PIN管理**  
  紙に書いて金庫保管、またはパスワードマネージャ（オフライン専用）で暗号化保存
- **自動復帰禁止**  
  意図的に手動操作を強制することで、自動化攻撃を防ぐ
- **監視強化**  
  `tuffutl log tail | grep Isolation` を常時監視（別端末で）

Isolationモードは「**一度発動したら、信頼できる管理者しか戻せない**」という、TUFF-OSの究極のFail-Closed哲学を体現しています。

ご不明な点や、特定のシナリオ（例：PIN紛失時の完全復旧フロー）についてさらに詳しく知りたい場合は、遠慮なくお知らせください。🛡️
