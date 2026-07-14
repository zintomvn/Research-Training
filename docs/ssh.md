# SSH: Cơ sở lý thuyết, kiến trúc và thực hành

## 1. Mục tiêu tài liệu

Tài liệu này trình bày SSH theo hướng lý thuyết kết hợp thực hành, giúp người học nắm được:

- SSH là gì và vì sao SSH được dùng cho đăng nhập từ xa, chạy lệnh từ xa và các dịch vụ mạng an toàn trên mạng không an toàn.
- Kiến trúc giao thức SSH gồm transport layer protocol, user authentication protocol và connection protocol.
- Vai trò của SSH client, SSH server, `ssh`, `sshd`, host key, user key, `known_hosts` và `authorized_keys`.
- Cách SSH thiết lập kênh mã hóa, xác thực máy chủ, xác thực người dùng và mở session.
- Cách dùng các lệnh OpenSSH cơ bản như `ssh`, `ssh-keygen`, `ssh-agent`, `ssh-add`, `scp` và `sftp`.
- Cách cấu hình SSH client bằng `~/.ssh/config`.
- Cách dùng port forwarding, jump host và một số tùy chọn debug thường gặp.
- Các lỗi thường gặp khi dùng SSH và cách kiểm tra theo tài liệu OpenSSH.

Tài liệu này chỉ tổng hợp và diễn giải từ các nguồn chính thức được liệt kê ở cuối tài liệu, chủ yếu là OpenSSH manual pages và RFC 4251-4254. Khi triển khai thực tế, cần kiểm tra đúng manual của hệ điều hành và phiên bản OpenSSH đang dùng, vì tùy chọn và thuật toán mặc định có thể thay đổi theo phiên bản.

## 2. Tổng quan về SSH

SSH là viết tắt của Secure Shell. Theo RFC 4251, SSH là giao thức dùng cho đăng nhập từ xa an toàn và các dịch vụ mạng an toàn khác trên mạng không an toàn. OpenSSH manual mô tả `ssh` là chương trình client để đăng nhập vào máy từ xa và chạy lệnh trên máy từ xa.

Trong thực tế, SSH thường xuất hiện dưới dạng mô hình client-server:

```text
Local machine -> ssh client -> network -> sshd server -> remote machine
```

Khi người dùng chạy:

```bash
ssh user@example.com
```

client `ssh` kết nối đến máy chủ, máy chủ `sshd` phản hồi bằng thông tin nhận dạng của host, hai bên thiết lập kênh bảo mật, sau đó người dùng chứng minh danh tính để được đăng nhập hoặc chạy lệnh.

SSH không chỉ dùng cho shell tương tác. Theo OpenSSH `ssh(1)`, SSH còn có thể:

- Chạy lệnh trên máy từ xa.
- Forward X11 connection.
- Forward TCP port.
- Forward Unix-domain socket.
- Tạo dynamic application-level port forwarding theo kiểu SOCKS.
- Kết nối qua jump host bằng `-J`.

Workflow cơ bản:

```text
Connect -> Verify host key -> Key exchange -> Encrypted channel -> User authentication -> Session/command/forwarding
```

## 3. Kiến trúc giao thức SSH

Theo RFC 4251, SSH gồm ba thành phần chính:

| Thành phần | Vai trò |
| --- | --- |
| Transport Layer Protocol | Xác thực máy chủ, bảo mật dữ liệu, toàn vẹn dữ liệu và có thể hỗ trợ nén. |
| User Authentication Protocol | Xác thực người dùng phía client với server. |
| Connection Protocol | Ghép nhiều logical channel bên trong tunnel đã mã hóa. |

Ba lớp này chạy theo thứ tự:

```text
Reliable data stream
  -> SSH Transport Layer Protocol
  -> SSH User Authentication Protocol
  -> SSH Connection Protocol
  -> Session / command / forwarding channels
```

RFC 4251 mô tả transport layer thường chạy trên TCP/IP, nhưng về mặt giao thức có thể chạy trên một reliable data stream khác. Sau khi secure transport layer được thiết lập, client gửi service request. Sau khi xác thực người dùng hoàn tất, connection protocol có thể tạo các channel cho shell, command, TCP forwarding hoặc X11 forwarding.

### 3.1. Transport Layer Protocol

Transport layer là lớp nền của SSH. Theo RFC 4253 và phần kiến trúc trong RFC 4251, lớp này xử lý:

- Trao đổi phiên bản giao thức.
- Thương lượng thuật toán.
- Key exchange.
- Xác thực host server.
- Thiết lập khóa dùng cho mã hóa và kiểm tra toàn vẹn dữ liệu.
- Tùy chọn nén nếu được thương lượng.

OpenSSH `sshd(8)` mô tả mỗi host có host-specific key dùng để nhận dạng host. Khi client kết nối, daemon phản hồi bằng public host key. Client so sánh host key với database của mình để kiểm tra host key có thay đổi hay không.

### 3.2. User Authentication Protocol

Sau khi transport layer an toàn được thiết lập, user authentication protocol xác thực người dùng. RFC 4252 định nghĩa giao thức xác thực người dùng chạy trên SSH transport layer.

Trong OpenSSH, các cách xác thực phổ biến được thể hiện qua manual và cấu hình như:

- Public key authentication.
- Password authentication.
- Keyboard-interactive authentication.
- Host-based authentication.

Tùy server và cấu hình, một hoặc nhiều phương thức xác thực có thể được yêu cầu theo chính sách cục bộ.

### 3.3. Connection Protocol

RFC 4254 định nghĩa SSH connection protocol. Lớp này chạy trên user authentication protocol và tạo nhiều logical channel bên trong một kết nối đã mã hóa.

Các channel có thể phục vụ:

- Interactive shell.
- Chạy command từ xa.
- Subsystem như SFTP.
- TCP port forwarding.
- X11 forwarding.

Ý tưởng quan trọng là sau khi đã có một kết nối SSH an toàn, connection protocol có thể dùng kết nối đó cho nhiều mục đích thay vì chỉ một shell.

## 4. Các thành phần trong hệ sinh thái OpenSSH

OpenSSH cung cấp nhiều chương trình liên quan đến SSH. Các chương trình dưới đây được mô tả trong manual pages chính thức của OpenSSH.

| Công cụ | Vai trò |
| --- | --- |
| `ssh` | SSH client dùng để đăng nhập hoặc chạy lệnh trên máy từ xa. |
| `sshd` | SSH daemon/server, lắng nghe kết nối từ client. |
| `ssh-keygen` | Tạo, quản lý và chuyển đổi authentication key. |
| `ssh-agent` | Giữ private key dùng cho public key authentication. |
| `ssh-add` | Thêm private key identity vào `ssh-agent`. |
| `scp` | Copy file giữa các host qua SSH. |
| `sftp` | File transfer program chạy trên SSH. |
| `ssh_config` | File cấu hình client SSH. |
| `sshd_config` | File cấu hình server SSH. |

Luồng dùng OpenSSH đơn giản:

```text
ssh-keygen -> tạo key pair
public key -> thêm vào authorized_keys trên server
private key -> giữ ở client
ssh / ssh-agent / ssh-add -> dùng key để xác thực
```

## 5. Host key, user key và trust

SSH có hai nhóm key rất dễ nhầm:

| Loại key | Nằm ở đâu | Dùng để làm gì |
| --- | --- | --- |
| Host key | Server | Nhận dạng máy chủ SSH. |
| User authentication key | User/client | Chứng minh danh tính người dùng khi đăng nhập. |

### 5.1. Host key

Theo RFC 4251, server host nên có host key. Host key được dùng trong key exchange để client kiểm tra mình đang nói chuyện với đúng server.

OpenSSH `sshd(8)` mô tả client so sánh host key server gửi về với database của client. Trong OpenSSH, database người dùng thường là:

```text
~/.ssh/known_hosts
```

Nếu host key thay đổi so với dữ liệu đã biết, client có lý do để cảnh báo vì thay đổi đó có thể là thay đổi hợp lệ của server hoặc dấu hiệu rủi ro bảo mật.

### 5.2. Trust model của host key

RFC 4251 nêu hai mô hình tin cậy cho host key:

| Mô hình | Ý nghĩa |
| --- | --- |
| Local database | Client lưu ánh xạ hostname với public host key tương ứng. |
| Certification authority | Host key được chứng nhận bởi CA mà client tin cậy. |

RFC 4251 cũng nêu rằng việc không kiểm tra host key ở lần kết nối đầu tiên giúp dễ dùng hơn nhưng làm kết nối dễ bị tấn công man-in-the-middle chủ động. Vì vậy, khi làm việc với hệ thống quan trọng, nên xác minh fingerprint hoặc dùng cơ chế tin cậy phù hợp thay vì bỏ qua cảnh báo host key.

### 5.3. User authentication key

User authentication key là key pair của người dùng. OpenSSH `ssh-keygen(1)` dùng để tạo authentication key. Private key giữ ở client; public key có thể được đặt trên server trong file `authorized_keys` của user cần đăng nhập.

Theo `sshd(8)`, file:

```text
~/.ssh/authorized_keys
```

liệt kê public keys có thể dùng để đăng nhập với tư cách user đó. Mỗi dòng chứa một key; dòng trống và dòng bắt đầu bằng `#` được bỏ qua như comment.

## 6. Các file và thư mục quan trọng

OpenSSH dùng các file mặc định khác nhau cho client và server.

| Đường dẫn | Vai trò |
| --- | --- |
| `~/.ssh/` | Vị trí mặc định cho cấu hình và thông tin xác thực riêng của user. |
| `~/.ssh/config` | File cấu hình SSH client của user. |
| `/etc/ssh/ssh_config` | File cấu hình SSH client toàn hệ thống. |
| `~/.ssh/known_hosts` | Danh sách host key của các host mà user đã đăng nhập nếu chưa có trong danh sách toàn hệ thống. |
| `~/.ssh/authorized_keys` | Danh sách public key được phép đăng nhập vào user trên server. |
| `/etc/ssh/sshd_config` | File cấu hình SSH server. |
| `/etc/ssh/ssh_host_ecdsa_key` | Private host key ECDSA của server nếu được dùng. |
| `/etc/ssh/ssh_host_ed25519_key` | Private host key Ed25519 của server nếu được dùng. |
| `/etc/ssh/ssh_host_rsa_key` | Private host key RSA của server nếu được dùng. |

Theo `sshd(8)`, `~/.ssh/` nên chỉ cho user đọc/ghi/thực thi và không cho người khác truy cập. `authorized_keys` nên cho user đọc/ghi và không cho người khác truy cập. Nếu `authorized_keys`, thư mục `~/.ssh` hoặc home directory có quyền ghi bởi user khác, `sshd` có thể không cho dùng file đó trừ khi `StrictModes` được đặt thành `no`.

## 7. Luồng kết nối SSH

Một kết nối SSH có thể được hiểu theo luồng sau:

```mermaid
sequenceDiagram
    participant C as SSH client
    participant S as SSH server / sshd
    C->>S: Connect to destination
    S-->>C: Send host public key
    C->>C: Check known_hosts / trust policy
    C<->>S: Key exchange and algorithm negotiation
    C<->>S: Establish encrypted transport
    C->>S: User authentication request
    S-->>C: Authentication success or failure
    C->>S: Open session / command / forwarding channel
```

Các bước chính:

1. Client kết nối đến destination.
2. Server gửi public host key.
3. Client kiểm tra host key theo database hoặc trust policy.
4. Hai bên thương lượng thuật toán và thực hiện key exchange.
5. Transport layer bảo mật được thiết lập.
6. User authentication protocol xác thực người dùng.
7. Connection protocol mở channel cho shell, command, subsystem hoặc forwarding.

## 8. Dùng lệnh `ssh`

Cú pháp tổng quát theo `ssh(1)`:

```bash
ssh [options] destination [command [argument ...]]
```

`destination` có thể ở dạng:

```text
[user@]hostname
ssh://[user@]hostname[:port]
```

### 8.1. Đăng nhập vào máy từ xa

```bash
ssh user@example.com
```

Nếu không truyền command, `ssh` thường mở login shell trên remote host sau khi xác thực thành công.

### 8.2. Chạy lệnh từ xa

Theo `ssh(1)`, nếu command được chỉ định, command đó sẽ chạy trên remote host thay vì mở login shell.

```bash
ssh user@example.com hostname
```

Ví dụ chạy một lệnh có tham số:

```bash
ssh user@example.com "uname -a"
```

### 8.3. Chọn user, port và identity file

```bash
ssh -l user example.com
ssh -p 2222 user@example.com
ssh -i ~/.ssh/id_ed25519 user@example.com
```

Ý nghĩa:

| Tùy chọn | Ý nghĩa theo OpenSSH manual |
| --- | --- |
| `-l` | Chỉ định login name trên remote machine. |
| `-p` | Chỉ định port kết nối đến remote host. |
| `-i` | Chọn identity file dùng cho public key authentication. |

### 8.4. Debug kết nối

`ssh(1)` mô tả `-v` là verbose mode, hữu ích khi debug vấn đề kết nối, xác thực và cấu hình. Có thể tăng độ chi tiết bằng nhiều `-v`.

```bash
ssh -v user@example.com
ssh -vv user@example.com
ssh -vvv user@example.com
```

`-G` in cấu hình sau khi đã evaluate các block `Host` và `Match`, rồi thoát:

```bash
ssh -G example.com
```

## 9. Tạo và dùng SSH key

### 9.1. Tạo key bằng `ssh-keygen`

`ssh-keygen(1)` là công cụ tạo, quản lý và chuyển đổi authentication key cho OpenSSH.

Ví dụ tạo key Ed25519:

```bash
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519
```

Ví dụ tạo key RSA với số bit chỉ định:

```bash
ssh-keygen -t rsa -b 3072 -f ~/.ssh/id_rsa
```

Các file thường tạo ra:

| File | Ý nghĩa |
| --- | --- |
| `~/.ssh/id_ed25519` | Private key. |
| `~/.ssh/id_ed25519.pub` | Public key tương ứng. |

Private key không nên đưa cho server hoặc chia sẻ cho người khác. Public key là phần có thể đặt vào `authorized_keys` để server nhận biết key được phép đăng nhập.

### 9.2. Thêm public key vào server

Theo `sshd(8)`, `authorized_keys` chứa public keys được dùng để đăng nhập vào user tương ứng. Một cách làm thủ công là đưa nội dung file `.pub` vào:

```text
~/.ssh/authorized_keys
```

Ví dụ dạng dòng trong `authorized_keys`:

```text
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAA... user-comment
```

`sshd(8)` mô tả public key trong file này gồm các trường phân tách bằng khoảng trắng: options, keytype, base64-encoded key, comment. Trường options là tùy chọn; trường comment không được dùng cho xác thực nhưng tiện để người dùng nhận diện key.

### 9.3. Dùng key để đăng nhập

```bash
ssh -i ~/.ssh/id_ed25519 user@example.com
```

Nếu key ở đường dẫn mặc định hoặc đã nằm trong agent, có thể không cần `-i`:

```bash
ssh user@example.com
```

Theo `ssh(1)` và `ssh_config(5)`, các identity mặc định có thể gồm `~/.ssh/id_rsa`, `~/.ssh/id_ecdsa`, `~/.ssh/id_ecdsa_sk`, `~/.ssh/id_ed25519` và `~/.ssh/id_ed25519_sk`.

## 10. `ssh-agent` và `ssh-add`

`ssh-agent(1)` là chương trình giữ private key dùng cho public key authentication. Agent được tìm qua environment variables và có thể được `ssh` dùng tự động khi đăng nhập sang máy khác.

Luồng cơ bản:

```text
start ssh-agent -> ssh-add private key -> ssh uses agent during authentication
```

Khởi động agent trong shell kiểu Bourne:

```bash
eval "$(ssh-agent -s)"
```

Thêm key vào agent:

```bash
ssh-add ~/.ssh/id_ed25519
```

Liệt kê fingerprint của identity trong agent:

```bash
ssh-add -l
```

Xóa tất cả identity khỏi agent:

```bash
ssh-add -D
```

Theo `ssh-add(1)`, agent phải đang chạy và biến môi trường `SSH_AUTH_SOCK` phải chứa tên socket của agent để `ssh-add` hoạt động.

### 10.1. Agent forwarding

`ssh -A` bật forwarding kết nối đến authentication agent. OpenSSH manual cảnh báo phải dùng agent forwarding cẩn thận: người có khả năng truy cập socket agent trên remote host có thể dùng agent để thực hiện thao tác xác thực bằng identity đã load, dù họ không lấy được private key material từ agent.

Vì vậy, chỉ bật agent forwarding khi cần:

```bash
ssh -A user@example.com
```

Khi chỉ cần đi qua jump host, OpenSSH manual nêu `-J` là lựa chọn có thể an toàn hơn trong nhiều trường hợp.

## 11. Cấu hình SSH client

Theo `ssh_config(5)`, `ssh` lấy cấu hình theo thứ tự:

1. Command-line options.
2. User configuration file: `~/.ssh/config`.
3. System-wide configuration file: `/etc/ssh/ssh_config`.

Trừ khi được nói khác, giá trị đầu tiên của mỗi directive sẽ được dùng. Vì vậy, cấu hình cụ thể cho host nên đặt gần đầu file, còn mặc định chung nên đặt cuối file.

### 11.1. Cấu hình host cơ bản

Ví dụ:

```sshconfig
Host lab
    HostName example.com
    User student
    Port 2222
    IdentityFile ~/.ssh/id_ed25519
```

Sau đó có thể kết nối bằng alias:

```bash
ssh lab
```

Ý nghĩa một số directive:

| Directive | Ý nghĩa |
| --- | --- |
| `Host` | Giới hạn các khai báo tiếp theo cho host pattern tương ứng. |
| `HostName` | Tên host thật để đăng nhập. |
| `User` | User dùng để đăng nhập. |
| `Port` | Port kết nối đến remote host. |
| `IdentityFile` | File identity dùng cho public key authentication. |
| `IdentitiesOnly` | Chỉ dùng identity/certificate đã cấu hình, hữu ích khi agent có nhiều identity. |

### 11.2. Cấu hình nhiều host

```sshconfig
Host gpu-lab
    HostName gpu.example.com
    User researcher
    IdentityFile ~/.ssh/id_ed25519

Host *
    ServerAliveInterval 60
    HashKnownHosts yes
```

`Host *` có thể dùng để đặt mặc định chung cho mọi host. Theo `ssh_config(5)`, pattern `*` khớp với mọi host.

### 11.3. Kiểm tra cấu hình hiệu lực

```bash
ssh -G gpu-lab
```

Lệnh này hữu ích để xem sau khi áp dụng `Host`, `Match` và các giá trị mặc định, `ssh` thực sự dùng cấu hình nào.

## 12. Port forwarding

OpenSSH `ssh(1)` mô tả nhiều kiểu forwarding qua secure channel.

### 12.1. Local forwarding với `-L`

`-L` chỉ định rằng kết nối đến một TCP port hoặc Unix socket ở phía local client sẽ được forward qua secure channel đến host/port ở phía remote.

Ví dụ:

```bash
ssh -L 8080:localhost:80 user@example.com
```

Ý nghĩa logic:

```text
local client port 8080 -> SSH tunnel -> remote side connects to localhost:80
```

### 12.2. Remote forwarding với `-R`

`-R` chỉ định rằng kết nối đến một TCP port hoặc Unix socket ở phía remote server sẽ được forward về phía local.

Ví dụ:

```bash
ssh -R 9000:localhost:3000 user@example.com
```

Ý nghĩa logic:

```text
remote server port 9000 -> SSH tunnel -> local client connects to localhost:3000
```

Theo `ssh(1)`, remote bind address có thể bị hạn chế bởi cấu hình server, ví dụ `GatewayPorts`.

### 12.3. Dynamic forwarding với `-D`

`-D` tạo local dynamic application-level port forwarding. Theo `ssh(1)`, `ssh` sẽ hoạt động như SOCKS server và hiện hỗ trợ SOCKS4 và SOCKS5.

Ví dụ:

```bash
ssh -D 1080 user@example.com
```

Ý nghĩa logic:

```text
local SOCKS port 1080 -> SSH tunnel -> destination chosen by SOCKS client
```

### 12.4. Không chạy command khi chỉ forward port

`-N` yêu cầu không chạy remote command. Theo `ssh(1)`, tùy chọn này hữu ích khi chỉ dùng port forwarding.

```bash
ssh -N -L 8080:localhost:80 user@example.com
```

## 13. Jump host và ProxyJump

`ssh -J` kết nối đến target host bằng cách trước tiên tạo kết nối SSH đến jump host, rồi thiết lập TCP forwarding từ jump host đến destination cuối.

Ví dụ:

```bash
ssh -J bastion.example.com user@internal.example.com
```

Nhiều jump hop có thể phân tách bằng dấu phẩy:

```bash
ssh -J jump1.example.com,jump2.example.com user@target.example.com
```

Trong `~/.ssh/config`, directive tương ứng là `ProxyJump`:

```sshconfig
Host internal
    HostName internal.example.com
    User app
    ProxyJump bastion.example.com
```

Theo `ssh_config(5)`, cấu hình của destination host không tự động áp dụng cho jump host; nếu jump host cần cấu hình riêng thì nên khai báo riêng trong `~/.ssh/config`.

## 14. Copy file qua SSH

OpenSSH cung cấp `scp` và `sftp` cho file transfer qua SSH.

### 14.1. `scp`

`scp(1)` là chương trình copy file giữa các host trên mạng. Ví dụ:

```bash
scp local.txt user@example.com:/tmp/local.txt
```

Copy từ remote về local:

```bash
scp user@example.com:/tmp/report.txt ./report.txt
```

### 14.2. `sftp`

`sftp(1)` là file transfer program. Có thể mở phiên tương tác:

```bash
sftp user@example.com
```

Một số thao tác thường dùng trong phiên `sftp`:

```text
ls
pwd
cd /tmp
put local.txt
get remote.txt
bye
```

`ssh(1)` cũng mô tả subsystem có thể dùng SSH như transport an toàn cho ứng dụng khác; SFTP là một ví dụ phổ biến trong OpenSSH manual.

## 15. Bảo mật và chính sách cần chú ý

### 15.1. Không bỏ qua host key một cách tùy tiện

RFC 4251 nêu rằng không kiểm tra host key trong lần kết nối đầu tiên làm kết nối dễ bị tấn công man-in-the-middle chủ động. OpenSSH dùng `known_hosts` để lưu và kiểm tra host key cho các lần sau.

Khi gặp cảnh báo host key thay đổi, không nên xóa dòng trong `known_hosts` nếu chưa xác minh vì đó có thể là thay đổi hợp lệ hoặc dấu hiệu bị can thiệp.

### 15.2. Giữ private key đúng quyền truy cập

Theo `ssh-add(1)`, identity files không nên readable bởi ai ngoài user; `ssh-add` bỏ qua identity files nếu chúng accessible bởi người khác.

Theo `sshd(8)`, private host key trên server chỉ nên owned by root, readable only by root và không accessible với người khác; `sshd` không start nếu các file này group/world-accessible.

### 15.3. Hạn chế agent forwarding

Agent forwarding tiện nhưng có rủi ro. OpenSSH `ssh(1)` ghi rõ người có khả năng bypass permission trên remote host có thể truy cập local agent qua forwarded connection và dùng identity đã load để xác thực.

Nếu mục tiêu là đi qua máy trung gian, cân nhắc dùng `ProxyJump` thay vì bật `ForwardAgent` rộng rãi.

### 15.4. Kiểm soát port forwarding

RFC 4251 nêu việc cho phép forward TCP/IP port là vấn đề chính sách cục bộ và có thể liên quan đến firewall. OpenSSH có các cấu hình như `GatewayPorts`, `LocalForward`, `RemoteForward`, `PermitOpen` hoặc tùy chọn trong `authorized_keys` để giới hạn forwarding.

## 16. Các lỗi thường gặp

### 16.1. Sai user hoặc hostname

Dấu hiệu:

```text
Could not resolve hostname ...
Permission denied ...
```

Kiểm tra:

```bash
ssh -v user@example.com
ssh -G example.com
```

`-v` giúp xem quá trình kết nối/xác thực; `-G` giúp xem cấu hình client thực tế.

### 16.2. Dùng sai private key

Dấu hiệu phổ biến là server từ chối xác thực public key.

Kiểm tra:

```bash
ssh -i ~/.ssh/id_ed25519 -v user@example.com
ssh-add -l
```

Nếu agent chứa quá nhiều identity, `IdentitiesOnly yes` trong `~/.ssh/config` có thể giúp buộc `ssh` chỉ dùng identity đã cấu hình.

### 16.3. Quyền file SSH không phù hợp

Theo `sshd(8)`, nếu `authorized_keys`, `~/.ssh` hoặc home directory writable bởi user khác, `sshd` có thể không cho dùng file đó khi `StrictModes` đang bật.

Quyền thường dùng trên hệ Unix:

```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
chmod 600 ~/.ssh/id_ed25519
```

Các lệnh trên phù hợp với khuyến nghị trong manual rằng các file/thư mục nhạy cảm chỉ nên cho user tương ứng truy cập.

### 16.4. Host key thay đổi

Dấu hiệu thường là cảnh báo về remote host identification hoặc host key mismatch.

Xử lý đúng:

1. Xác minh với quản trị viên hoặc nguồn tin cậy xem server có đổi host key không.
2. Nếu thay đổi hợp lệ, cập nhật `known_hosts`.
3. Nếu không xác minh được, không nên bỏ qua cảnh báo.

### 16.5. Port forwarding không hoạt động

Kiểm tra:

- Có dùng đúng `-L`, `-R` hoặc `-D` không.
- Có cần `-N` nếu chỉ forward port không.
- Remote service có lắng nghe ở host/port đích không.
- Server có hạn chế `GatewayPorts`, remote forwarding hoặc các chính sách liên quan không.
- Dùng `ssh -v` để xem forwarding request có thành công không.

### 16.6. Agent không hoạt động

Dấu hiệu:

```text
Could not open a connection to your authentication agent
```

Theo `ssh-add(1)`, agent phải chạy và `SSH_AUTH_SOCK` phải trỏ đến socket của agent.

Kiểm tra:

```bash
echo "$SSH_AUTH_SOCK"
ssh-add -l
```

Khởi động lại agent nếu cần:

```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

## 17. Thực hành cơ bản

### Bài 1: Kết nối SSH

Kết nối đến một host bằng dạng:

```bash
ssh user@example.com
```

Sau đó chạy thử một command từ xa:

```bash
ssh user@example.com hostname
```

### Bài 2: Tạo key pair

Tạo key Ed25519:

```bash
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519
```

Kiểm tra hai file được tạo:

```text
~/.ssh/id_ed25519
~/.ssh/id_ed25519.pub
```

### Bài 3: Cấu hình alias trong `~/.ssh/config`

Tạo cấu hình:

```sshconfig
Host lab
    HostName example.com
    User student
    IdentityFile ~/.ssh/id_ed25519
```

Kết nối:

```bash
ssh lab
```

Kiểm tra cấu hình hiệu lực:

```bash
ssh -G lab
```

### Bài 4: Dùng `ssh-agent`

Khởi động agent và thêm key:

```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
ssh-add -l
```

### Bài 5: Local port forwarding

Tạo local forwarding:

```bash
ssh -N -L 8080:localhost:80 user@example.com
```

Mục tiêu của bài là hiểu hướng đi của kết nối:

```text
client localhost:8080 -> SSH tunnel -> server localhost:80
```

### Bài 6: Jump host

Kết nối qua jump host:

```bash
ssh -J bastion.example.com user@internal.example.com
```

Sau đó chuyển cấu hình sang `~/.ssh/config` bằng `ProxyJump`.

### Bài 7: Debug lỗi xác thực

Chạy:

```bash
ssh -vvv user@example.com
```

Ghi lại:

- Client đang đọc file cấu hình nào.
- Client đang thử identity nào.
- Server chấp nhận hay từ chối phương thức xác thực nào.

## 18. Lộ trình học đề xuất

1. Hiểu SSH client-server và mục tiêu bảo mật của SSH.
2. Học ba lớp chính trong RFC 4251: transport, user authentication và connection.
3. Học host key, `known_hosts` và lý do phải xác minh host key.
4. Học user key, public key authentication và `authorized_keys`.
5. Thực hành `ssh`, `ssh-keygen`, `ssh-agent` và `ssh-add`.
6. Học `~/.ssh/config` để quản lý nhiều host.
7. Học port forwarding với `-L`, `-R`, `-D` và `-N`.
8. Học jump host với `-J` và `ProxyJump`.
9. Học copy file bằng `scp` và `sftp`.
10. Học debug bằng `ssh -v`, `ssh -G` và kiểm tra quyền file.

## 19. Kết luận

SSH là giao thức nền tảng cho quản trị hệ thống, truy cập server, truyền file và tạo tunnel an toàn. Về mặt kiến trúc, SSH tách thành transport layer để tạo kênh bảo mật, user authentication protocol để xác thực người dùng và connection protocol để mở các logical channel như shell, command, subsystem hoặc port forwarding.

Trong OpenSSH, người dùng thường làm việc với `ssh`, `ssh-keygen`, `ssh-agent`, `ssh-add`, `scp`, `sftp` và các file trong `~/.ssh`. Để dùng SSH đúng cách, cần phân biệt host key với user key, không bỏ qua cảnh báo host key, giữ private key đúng quyền truy cập, cấu hình client rõ ràng bằng `~/.ssh/config` và dùng `ssh -v` khi cần debug.

## 20. Tài liệu tham khảo

- OpenSSH `ssh(1)`: https://man.openbsd.org/ssh
- OpenSSH `ssh_config(5)`: https://man.openbsd.org/ssh_config
- OpenSSH `sshd(8)`: https://man.openbsd.org/sshd
- OpenSSH `sshd_config(5)`: https://man.openbsd.org/sshd_config
- OpenSSH `ssh-keygen(1)`: https://man.openbsd.org/ssh-keygen
- OpenSSH `ssh-agent(1)`: https://man.openbsd.org/ssh-agent
- OpenSSH `ssh-add(1)`: https://man.openbsd.org/ssh-add
- OpenSSH `scp(1)`: https://man.openbsd.org/scp
- OpenSSH `sftp(1)`: https://man.openbsd.org/sftp
- RFC 4251 - The Secure Shell (SSH) Protocol Architecture: https://datatracker.ietf.org/doc/html/rfc4251
- RFC 4252 - The Secure Shell (SSH) Authentication Protocol: https://datatracker.ietf.org/doc/html/rfc4252
- RFC 4253 - The Secure Shell (SSH) Transport Layer Protocol: https://datatracker.ietf.org/doc/html/rfc4253
- RFC 4254 - The Secure Shell (SSH) Connection Protocol: https://datatracker.ietf.org/doc/html/rfc4254
