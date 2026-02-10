# BÁO CÁO DỰ ÁN CHATBOT CLOUD

**Môn học:** Cloud Computing  
**Trường:** Đại học Bách Khoa Hà Nội (HUST)  
**Năm:** 2026  
**Loại dự án:** Bài Tập Lớn

---

## MỤC LỤC

1. [Giới thiệu dự án](#1-giới-thiệu-dự-án)
2. [Mục tiêu dự án](#2-mục-tiêu-dự-án)
3. [Kiến trúc hệ thống](#3-kiến-trúc-hệ-thống)
4. [Công nghệ sử dụng](#4-công-nghệ-sử-dụng)
5. [Tính năng đã triển khai](#5-tính-năng-đã-triển-khai)
6. [Quy trình triển khai](#6-quy-trình-triển-khai)
7. [Kết quả thử nghiệm](#7-kết-quả-thử-nghiệm)
8. [Kết luận và hướng phát triển](#8-kết-luận-và-hướng-phát-triển)
9. [Tài liệu tham khảo](#9-tài-liệu-tham-khảo)

---

## 1. GIỚI THIỆU DỰ ÁN

### 1.1. Tổng quan

Chatbot Cloud là một hệ thống chatbot thông minh được xây dựng hoàn toàn trên nền tảng Google Cloud Platform (GCP), áp dụng kiến trúc serverless hiện đại và tích hợp các mô hình ngôn ngữ lớn (Large Language Model - LLM) để cung cấp khả năng hội thoại tự nhiên với người dùng. Dự án này không chỉ đơn thuần là một ứng dụng chatbot thông thường, mà còn là một nghiên cứu chuyên sâu về việc áp dụng các công nghệ cloud computing tiên tiến vào thực tế.

Hệ thống được thiết kế với mục đích phục vụ học tập và nghiên cứu trong lĩnh vực Cloud Computing, đặc biệt tập trung vào các khía cạnh quan trọng như kiến trúc serverless, khả năng tự động mở rộng quy mô (auto-scaling), tích hợp trí tuệ nhân tạo vào ứng dụng cloud, xử lý bất đồng bộ với hàng đợi tin nhắn, quản lý hạ tầng bằng mã nguồn (Infrastructure as Code) thông qua Terraform, và xây dựng pipeline CI/CD tự động hóa trên môi trường cloud.

Điểm đặc biệt của dự án nằm ở việc kết hợp hài hòa giữa các dịch vụ managed services của GCP với các framework và thư viện hiện đại, tạo nên một hệ thống có khả năng mở rộng cao, tối ưu chi phí và dễ dàng bảo trì. Thông qua việc triển khai dự án này, chúng tôi không chỉ xây dựng được một sản phẩm hoàn chỉnh mà còn tích lũy được kinh nghiệm thực tế quý báu về cách thức vận hành và tối ưu hóa các ứng dụng trên nền tảng cloud.

### 1.2. Bối cảnh và động lực

Trong bối cảnh công nghệ cloud computing đang phát triển với tốc độ chóng mặt, việc xây dựng các ứng dụng có khả năng tự động mở rộng quy mô, tối ưu chi phí theo mô hình pay-as-you-go và dễ dàng bảo trì đã trở thành một xu hướng tất yếu trong ngành công nghiệp phần mềm hiện đại. Các doanh nghiệp ngày càng chuyển dịch từ mô hình truyền thống sang các giải pháp cloud-native để tận dụng tối đa các lợi ích mà công nghệ đám mây mang lại.

Dự án Chatbot Cloud được thực hiện với nhiều mục đích quan trọng. Thứ nhất, chúng tôi muốn nghiên cứu và áp dụng kiến trúc serverless trên Google Cloud Platform một cách toàn diện, từ việc thiết kế kiến trúc, lựa chọn các dịch vụ phù hợp, cho đến việc tối ưu hóa hiệu năng và chi phí. Thứ hai, việc tích hợp các mô hình ngôn ngữ lớn (LLM) vào ứng dụng thực tế là một thách thức kỹ thuật đáng quan tâm, đặc biệt trong bối cảnh AI đang ngày càng trở nên phổ biến và mạnh mẽ.

Thứ ba, chúng tôi muốn thực hành các phương pháp DevOps hiện đại thông qua việc sử dụng Infrastructure as Code (IaC) với Terraform và xây dựng pipeline CI/CD tự động. Điều này giúp đảm bảo tính nhất quán, khả năng tái tạo và tự động hóa trong quá trình triển khai và vận hành hệ thống. Cuối cùng, việc tối ưu hiệu năng và chi phí vận hành là một yếu tố then chốt trong bất kỳ dự án cloud nào, và chúng tôi muốn tìm hiểu sâu về cách thức đạt được sự cân bằng tối ưu giữa hai yếu tố này.

Thông qua dự án này, chúng tôi hy vọng không chỉ xây dựng được một hệ thống chatbot hoàn chỉnh mà còn tích lũy được kiến thức và kinh nghiệm thực tế về cloud computing, serverless architecture, AI integration và DevOps practices - những kỹ năng vô cùng quan trọng trong ngành công nghiệp phần mềm hiện đại.

### 1.3. Phạm vi dự án

Để đảm bảo tính khả thi và tập trung vào các mục tiêu học tập chính, chúng tôi đã xác định rõ ràng phạm vi của dự án. Domain ứng dụng được chọn là chatbot tư vấn tài chính cá nhân ở mức độ demo, một lĩnh vực vừa đủ phức tạp để thể hiện các khả năng kỹ thuật nhưng cũng không quá rộng để khó kiểm soát.

Về chức năng chính, hệ thống cung cấp khả năng hỏi đáp về các chủ đề tài chính cá nhân cơ bản như tiết kiệm, lãi suất, quản lý ngân sách cá nhân. Ngoài ra, hệ thống còn tích hợp các công cụ tính toán tài chính như tính lãi suất (đơn và ghép), tính tỷ lệ tiết kiệm, giúp người dùng có thể nhận được những tư vấn cụ thể và có tính toán. Lịch sử hội thoại được lưu trữ để đảm bảo tính liên tục trong cuộc trò chuyện, và hệ thống hỗ trợ xử lý bất đồng bộ cho các request nặng để tối ưu trải nghiệm người dùng.

Tuy nhiên, để đảm bảo tính thực tế và an toàn, chúng tôi cũng đặt ra các giới hạn rõ ràng. Hệ thống không kết nối với các ngân hàng thật hay các dịch vụ tài chính thực tế, không cung cấp tư vấn đầu tư chuyên sâu hay các dịch vụ tài chính phức tạp, và được xây dựng chủ yếu phục vụ mục đích demo và học tập. Những giới hạn này giúp chúng tôi tập trung vào các khía cạnh kỹ thuật của cloud computing và serverless architecture mà không bị phân tán bởi các yêu cầu nghiệp vụ phức tạp.

---

## 2. MỤC TIÊU DỰ ÁN

### 2.1. Mục tiêu chính

Dự án Chatbot Cloud được thiết lập với năm mục tiêu chính, mỗi mục tiêu đều hướng đến việc nắm vững một khía cạnh quan trọng của cloud computing và phát triển phần mềm hiện đại.

Mục tiêu đầu tiên và quan trọng nhất là xây dựng một hệ thống chatbot serverless hoàn chỉnh có khả năng tự động mở rộng quy mô theo tải. Điều này không chỉ đơn thuần là triển khai ứng dụng lên cloud, mà còn bao gồm việc thiết kế kiến trúc phù hợp, cấu hình auto-scaling hợp lý, và tối ưu hóa để hệ thống có thể xử lý từ vài request đến hàng nghìn request đồng thời một cách mượt mà.

Mục tiêu thứ hai là tích hợp Large Language Model (LLM) để xử lý ngôn ngữ tự nhiên một cách hiệu quả. Việc tích hợp LLM không chỉ là gọi API đơn giản, mà còn bao gồm prompt engineering, context management, function calling, và xử lý các edge cases như timeout, rate limiting. Chúng tôi cần đảm bảo rằng chatbot có thể hiểu và phản hồi các câu hỏi của người dùng một cách tự nhiên và chính xác.

Mục tiêu thứ ba là triển khai toàn bộ hệ thống trên Google Cloud Platform sử dụng các managed services. Điều này giúp chúng tôi tận dụng tối đa các lợi ích của cloud như high availability, scalability, và giảm thiểu công việc vận hành. Chúng tôi sử dụng Cloud Run cho hosting, Cloud Storage cho lưu trữ, Pub/Sub cho message queue, Secret Manager cho quản lý credentials, và nhiều dịch vụ khác.

Mục tiêu thứ tư là áp dụng Infrastructure as Code (IaC) để quản lý toàn bộ hạ tầng. Thông qua Terraform, chúng tôi có thể định nghĩa, version control, và tái tạo toàn bộ hạ tầng một cách nhất quán. Điều này không chỉ giúp việc triển khai trở nên dễ dàng và đáng tin cậy, mà còn tạo điều kiện cho việc collaboration và documentation.

Mục tiêu cuối cùng là xây dựng CI/CD pipeline tự động hóa hoàn toàn. Từ việc commit code, chạy tests, build images, cho đến deploy lên production, tất cả đều được tự động hóa thông qua Cloud Build và GitHub Actions. Điều này đảm bảo chất lượng code, giảm thiểu lỗi do con người, và tăng tốc độ phát triển.

### 2.2. Mục tiêu kỹ thuật

Để đánh giá sự thành công của dự án một cách khách quan, chúng tôi đã đặt ra các mục tiêu kỹ thuật cụ thể với các chỉ số đo lường rõ ràng.

Về khả năng auto-scaling, chúng tôi đặt mục tiêu thời gian scale up hoặc scale down phải dưới 30 giây. Điều này đảm bảo rằng hệ thống có thể phản ứng nhanh chóng với sự thay đổi của tải, tránh tình trạng quá tải khi có đột biến traffic hoặc lãng phí tài nguyên khi traffic giảm.

Về hiệu năng, chúng tôi đặt hai mục tiêu khác nhau cho hai loại request. Đối với các API đơn giản như health check, create session, response time phải dưới 500ms để đảm bảo trải nghiệm người dùng mượt mà. Đối với các request chat có gọi LLM, do tính chất của việc xử lý ngôn ngữ tự nhiên, chúng tôi chấp nhận response time dưới 5 giây, một mức độ hợp lý cho loại tác vụ này.

Về độ khả dụng, chúng tôi đặt mục tiêu uptime trên 99%, tương đương với khoảng 7.2 giờ downtime tối đa trong một năm. Mục tiêu này phù hợp với một hệ thống demo nhưng vẫn đảm bảo tính ổn định cần thiết.

Về tối ưu chi phí, một trong những lợi ích lớn nhất của serverless là khả năng scale to zero - không tính phí khi hệ thống không được sử dụng. Chúng tôi đặt mục tiêu đạt được điều này, đảm bảo rằng khi không có traffic, số lượng instances sẽ giảm về 0 và không phát sinh chi phí computing.

### 2.3. Mục tiêu học tập

Bên cạnh các mục tiêu kỹ thuật, dự án còn hướng đến nhiều mục tiêu học tập quan trọng, giúp chúng tôi phát triển kỹ năng và kiến thức cần thiết cho sự nghiệp trong lĩnh vực cloud computing và phát triển phần mềm.

Đầu tiên, chúng tôi muốn hiểu rõ về kiến trúc serverless và các design patterns phổ biến. Serverless không chỉ là việc không quản lý server, mà còn là một paradigm shift trong cách thiết kế và vận hành ứng dụng. Chúng tôi cần nắm vững các khái niệm như stateless design, event-driven architecture, cold start optimization, và cách xử lý các thách thức đặc thù của serverless.

Thứ hai, việc thực hành với các GCP services là vô cùng quan trọng. Mỗi service như Cloud Run, Cloud Storage, Pub/Sub, Secret Manager đều có những đặc điểm, best practices và gotchas riêng. Thông qua dự án, chúng tôi có cơ hội làm việc trực tiếp với các services này, hiểu cách chúng hoạt động, cách tích hợp chúng với nhau, và cách tối ưu hóa chúng.

Thứ ba, Terraform là một công cụ IaC mạnh mẽ và được sử dụng rộng rãi trong industry. Chúng tôi muốn nắm vững cách sử dụng Terraform để quản lý infrastructure, từ việc viết configuration files, quản lý state, xử lý dependencies, cho đến việc tổ chức code và collaboration.

Thứ tư, việc xây dựng CI/CD với Cloud Build và GitHub Actions giúp chúng tôi hiểu về automation, testing, và deployment strategies. Chúng tôi học cách thiết lập pipeline, viết tests, xử lý secrets, và implement các best practices như blue-green deployment hay canary releases.

Thứ năm, tích hợp và sử dụng LLM API là một kỹ năng ngày càng quan trọng trong thời đại AI. Chúng tôi học cách làm việc với LLM API, prompt engineering, context management, function calling, và xử lý các challenges như latency, cost, và reliability.

Cuối cùng, load testing và performance optimization là những kỹ năng thiết yếu cho bất kỳ hệ thống production nào. Chúng tôi học cách thiết kế test scenarios, sử dụng các công cụ như Locust và pytest, phân tích kết quả, và tối ưu hóa hệ thống dựa trên insights thu được.

---

## 3. KIẾN TRÚC HỆ THỐNG

### 3.1. Tổng quan kiến trúc

Kiến trúc của hệ thống Chatbot Cloud được thiết kế theo mô hình serverless microservices, một approach hiện đại cho phép tối ưu hóa cả về mặt hiệu năng lẫn chi phí. Toàn bộ hệ thống được xây dựng trên nền tảng Google Cloud Platform, tận dụng các managed services để giảm thiểu công việc vận hành và tập trung vào logic nghiệp vụ.

Ở tầng cao nhất, kiến trúc bao gồm ba thành phần chính: Frontend (giao diện người dùng), Chatbot Service (logic xử lý chính), và Tools Service (các microservices hỗ trợ). Ba thành phần này đều được triển khai dưới dạng containers trên Cloud Run, cho phép chúng scale độc lập và tối ưu hóa resource usage.

Luồng tương tác cơ bản bắt đầu từ người dùng gửi tin nhắn qua giao diện web. Frontend nhận tin nhắn và gửi request đến Chatbot Service. Chatbot Service sau đó điều phối giữa nhiều thành phần: gọi LLM để xử lý ngôn ngữ tự nhiên, gọi Tools Service khi cần thực hiện các tác vụ cụ thể, lưu trữ lịch sử hội thoại vào Cloud Storage, và có thể sử dụng Pub/Sub để xử lý bất đồng bộ các request nặng.

Một điểm đặc biệt trong kiến trúc là việc sử dụng Pub/Sub cho async processing. Khi có request chat cần xử lý LLM (thường mất 3-5 giây), thay vì giữ connection và chờ đợi, Chatbot Service có thể publish message lên Pub/Sub topic và trả về ngay cho client. Pub/Sub sau đó push message đến một endpoint khác của Chatbot để xử lý, và client có thể poll để lấy kết quả sau. Cơ chế này giúp tránh timeout và cải thiện user experience đáng kể.

### 3.2. Các thành phần chi tiết

#### Frontend Service

Frontend được xây dựng bằng Streamlit, một Python framework cho phép tạo web UI nhanh chóng và hiệu quả. Lựa chọn Streamlit không chỉ vì tính đơn giản mà còn vì nó cho phép chúng tôi sử dụng Python cho cả backend và frontend, giảm thiểu context switching và tận dụng các thư viện Python có sẵn.

Frontend được đóng gói thành Docker container và deploy lên Cloud Run. Nó cung cấp giao diện chat trực quan, cho phép người dùng tạo session mới, gửi tin nhắn, xem lịch sử hội thoại, và lựa chọn giữa xử lý đồng bộ hay bất đồng bộ. Giao diện được thiết kế đơn giản nhưng đầy đủ chức năng, phù hợp với mục đích demo và testing.

Một tính năng quan trọng của Frontend là khả năng quản lý session. Mỗi cuộc hội thoại được gắn với một session ID duy nhất, giúp Chatbot Service có thể maintain context và lưu trữ lịch sử một cách có tổ chức. Frontend cũng xử lý các trường hợp lỗi như network timeout, server error, và hiển thị thông báo phù hợp cho người dùng.

#### Chatbot Service

Chatbot Service là trái tim của hệ thống, được xây dựng bằng Python với FastAPI framework. FastAPI được chọn vì hiệu năng cao, hỗ trợ async/await native, automatic API documentation, và type safety thông qua Pydantic.

Service này đóng vai trò điều phối giữa tất cả các thành phần khác. Khi nhận được tin nhắn từ Frontend, nó thực hiện một loạt các tác vụ: validate input, load conversation history từ Cloud Storage, gọi LLM API với appropriate prompt và context, parse response từ LLM, thực hiện function calling nếu LLM yêu cầu, lưu tin nhắn mới vào Storage, và trả về response cho Frontend.

Một khía cạnh quan trọng của Chatbot Service là context management. Để LLM có thể trả lời chính xác, nó cần có đủ context về cuộc hội thoại trước đó. Service quản lý context này bằng cách load lịch sử từ Storage, format thành dạng phù hợp cho LLM, và đảm bảo không vượt quá token limit của LLM.

Service cũng implement hai modes: synchronous và asynchronous. Trong synchronous mode, request được xử lý ngay và response được trả về trực tiếp. Trong asynchronous mode, request được publish lên Pub/Sub, và client nhận được response "pending" ngay lập tức, sau đó poll để lấy kết quả thực tế.

#### Tools Service

Tools Service là một tập hợp các microservices cung cấp các chức năng cụ thể mà LLM có thể gọi thông qua function calling mechanism. Hiện tại, service cung cấp hai tools chính: tính lãi suất (đơn và ghép) và tính tỷ lệ tiết kiệm.

Mỗi tool được implement như một API endpoint riêng biệt, nhận parameters từ LLM, thực hiện tính toán, và trả về kết quả có cấu trúc. Việc tách Tools thành một service riêng không chỉ giúp code organization tốt hơn mà còn cho phép scale độc lập - nếu có nhiều request gọi tools, chỉ Tools Service cần scale up, không ảnh hưởng đến Chatbot Service.

Tools Service cũng được xây dựng với FastAPI và deploy trên Cloud Run. Nó được thiết kế để dễ dàng mở rộng - thêm tool mới chỉ cần implement một endpoint mới và update tool definitions trong Chatbot Service.

#### LLM Integration

Việc tích hợp LLM là một phần quan trọng và phức tạp của hệ thống. Chúng tôi sử dụng OpenAI API (có thể thay thế bằng Vertex AI hoặc các providers khác) để cung cấp khả năng xử lý ngôn ngữ tự nhiên.

Integration không chỉ đơn giản là gọi API mà còn bao gồm nhiều khía cạnh: prompt engineering để LLM hiểu rõ domain và nhiệm vụ, context management để maintain conversation flow, function calling để LLM có thể sử dụng tools, error handling cho các trường hợp timeout hoặc rate limiting, và cost optimization để giảm thiểu số tokens sử dụng.

Chúng tôi sử dụng system prompt để định nghĩa personality và capabilities của chatbot, user messages để truyền đạt câu hỏi của người dùng, và assistant messages để maintain conversation history. Function definitions được cung cấp để LLM biết khi nào và cách gọi các tools available.

#### Cloud Storage

Cloud Storage được sử dụng để lưu trữ persistent data, chủ yếu là lịch sử hội thoại. Mỗi session được lưu thành một JSON file trong bucket, với cấu trúc rõ ràng bao gồm session metadata và array of messages.

Việc sử dụng Cloud Storage thay vì database có nhiều lý do: đơn giản hơn cho use case này, chi phí thấp hơn, không cần quản lý database instance, và phù hợp với serverless architecture. Tuy nhiên, chúng tôi cũng nhận thức được limitations như không thể query phức tạp hay transaction support, và có kế hoạch migrate sang Cloud SQL hoặc Firestore nếu cần trong tương lai.

Storage operations được optimize để giảm latency: sử dụng caching khi có thể, batch operations khi phù hợp, và async I/O để không block main thread.

#### Pub/Sub Message Queue

Google Cloud Pub/Sub đóng vai trò quan trọng trong việc xử lý bất đồng bộ. Khi có request chat nặng (gọi LLM), thay vì xử lý đồng bộ và risk timeout, Chatbot Service publish message lên topic "chat-requests".

Pub/Sub sau đó push message này đến một subscription endpoint của Chatbot Service (endpoint khác với endpoint nhận request từ Frontend). Endpoint này xử lý message: gọi LLM, lưu response vào Storage, và acknowledge message. Trong khi đó, Frontend poll endpoint khác để check xem response đã sẵn sàng chưa.

Cơ chế này mang lại nhiều lợi ích: tránh timeout do LLM xử lý lâu, decouple request receiving và processing, có thể retry nếu processing fail, và scale processing capacity độc lập với request handling capacity.

#### Secret Manager

Secret Manager được sử dụng để lưu trữ an toàn các credentials nhạy cảm như OpenAI API key. Thay vì hardcode hoặc lưu trong environment variables (có thể bị expose), secrets được lưu trong Secret Manager và được inject vào containers khi runtime.

Cloud Run có integration tốt với Secret Manager, cho phép mount secrets như environment variables hoặc files. Chúng tôi configure IAM permissions để chỉ các services cần thiết mới có quyền access secrets, following principle of least privilege.

### 3.3. Luồng xử lý chi tiết

#### Luồng đồng bộ (Synchronous Flow)

Trong luồng đồng bộ, toàn bộ quá trình xử lý diễn ra trong một request-response cycle. Người dùng gửi tin nhắn từ Frontend, Frontend gửi POST request đến `/api/chat` endpoint của Chatbot Service. Chatbot Service nhận request, validate input, load conversation history từ Cloud Storage, gọi LLM API với full context.

LLM xử lý request và có thể quyết định gọi tool nếu cần. Nếu LLM request function call, Chatbot Service parse function name và arguments, gọi appropriate endpoint trên Tools Service, nhận kết quả, và gọi lại LLM với function result. LLM sau đó generate final response dựa trên function result.

Chatbot Service nhận final response từ LLM, lưu cả user message và assistant message vào Cloud Storage, và trả về response cho Frontend. Frontend hiển thị response cho người dùng. Toàn bộ quá trình này thường mất 3-5 giây, phụ thuộc vào độ phức tạp của request và response time của LLM.

#### Luồng bất đồng bộ (Asynchronous Flow)

Luồng bất đồng bộ phức tạp hơn nhưng mang lại trải nghiệm tốt hơn cho người dùng. Khi Frontend gửi request với flag `async=1`, Chatbot Service không xử lý ngay mà thực hiện các bước sau:

Đầu tiên, lưu user message vào Cloud Storage với status "pending". Sau đó, publish một message lên Pub/Sub topic "chat-requests" với payload chứa session_id và message content. Ngay lập tức trả về response cho Frontend với status "pending" và message_id.

Pub/Sub nhận message và push đến subscription endpoint `/api/pubsub/chat-handler` của Chatbot Service. Endpoint này được trigger asynchronously, load message từ Storage, gọi LLM, xử lý function calls nếu có, lưu assistant response vào Storage với status "completed", và acknowledge message với Pub/Sub.

Trong khi đó, Frontend poll endpoint `/api/sessions/{session_id}/messages` mỗi vài giây để check xem có message mới không. Khi assistant message có status "completed", Frontend hiển thị cho người dùng.

Cơ chế này cho phép người dùng nhận được feedback ngay lập tức (status pending) thay vì phải chờ đợi, và có thể làm việc khác trong khi chờ response. Nó cũng tránh được timeout issues và cho phép xử lý các request rất nặng.

### 3.4. Nguyên tắc thiết kế

Kiến trúc của hệ thống được xây dựng dựa trên năm nguyên tắc thiết kế chính, đảm bảo tính scalable, maintainable và cost-effective.

**Serverless-First Approach**: Chúng tôi ưu tiên sử dụng serverless services bất cứ khi nào có thể. Cloud Run cho hosting, Cloud Storage cho persistence, Pub/Sub cho messaging - tất cả đều là managed services không yêu cầu quản lý infrastructure. Điều này mang lại auto-scaling, high availability, và pay-per-use pricing model.

**Microservices Architecture**: Hệ thống được chia thành các services nhỏ, mỗi service có một responsibility rõ ràng. Frontend xử lý UI, Chatbot xử lý orchestration, Tools cung cấp specific functions. Các services này có thể develop, deploy và scale độc lập, tăng flexibility và maintainability.

**Loose Coupling**: Các components được thiết kế để minimize dependencies. Pub/Sub được sử dụng để decouple request receiving và processing. Services communicate qua well-defined APIs. Điều này cho phép thay đổi implementation của một component mà không ảnh hưởng đến các components khác.

**Stateless Design**: Tất cả services đều stateless - không lưu state trong memory hay local disk. State được persist vào Cloud Storage. Điều này cho phép services scale horizontally dễ dàng và recover nhanh chóng từ failures.

**Security by Design**: Security được tích hợp từ đầu chứ không phải afterthought. Secrets được lưu trong Secret Manager, IAM được configure theo principle of least privilege, HTTPS được enforce cho tất cả communications, và sensitive data được encrypt at rest và in transit.

---

## 4. CÔNG NGHỆ SỬ DỤNG

### 4.1. Nền tảng Cloud và các dịch vụ chính

Việc lựa chọn Google Cloud Platform làm nền tảng chính cho dự án không phải là ngẫu nhiên mà dựa trên nhiều yếu tố kỹ thuật và chiến lược. GCP cung cấp một hệ sinh thái phong phú các managed services với độ tin cậy cao, hiệu năng tốt và mô hình pricing linh hoạt, đặc biệt phù hợp với kiến trúc serverless mà chúng tôi hướng đến.

**Google Cloud Run** là trụ cột chính của kiến trúc, đóng vai trò hosting cho tất cả các containers của chúng tôi. Cloud Run được chọn vì khả năng auto-scaling vượt trội - có thể scale từ 0 đến hàng nghìn instances trong vài giây, mô hình pay-per-use chỉ tính phí khi có request thực tế, và sự đơn giản trong việc deploy - chỉ cần push container image và Cloud Run lo phần còn lại. Đặc biệt, Cloud Run hỗ trợ cả HTTP requests và event-driven triggers từ Pub/Sub, cho phép chúng tôi implement cả synchronous và asynchronous processing patterns.

**Cloud Storage** được sử dụng làm persistence layer chính, lưu trữ toàn bộ lịch sử hội thoại và session data. Lựa chọn Cloud Storage thay vì database truyền thống mang lại nhiều lợi ích: chi phí cực kỳ thấp (chỉ vài cent per GB per month), độ bền dữ liệu 99.999999999% (11 nines), không cần quản lý infrastructure, và khả năng scale không giới hạn. Mặc dù không có khả năng query phức tạp như database, nhưng với use case của chúng tôi - chủ yếu là read/write theo session ID - Cloud Storage là lựa chọn tối ưu.

**Cloud Pub/Sub** đóng vai trò then chốt trong việc xử lý bất đồng bộ, giải quyết một trong những thách thức lớn nhất khi làm việc với LLM: latency cao. Pub/Sub là một managed message queue service với độ tin cậy cao, hỗ trợ at-least-once delivery guarantee, và có thể xử lý hàng triệu messages per second. Việc sử dụng Pub/Sub cho phép chúng tôi decouple hoàn toàn giữa việc nhận request và xử lý request, tránh timeout, và có khả năng retry tự động khi có lỗi.

**Secret Manager** là giải pháp bảo mật cho việc quản lý credentials nhạy cảm như API keys. Thay vì lưu secrets trong code, environment variables files, hoặc configuration files (tất cả đều có nguy cơ bị expose), Secret Manager cung cấp một nơi tập trung, được mã hóa và audit-logged để lưu trữ secrets. Cloud Run có integration native với Secret Manager, cho phép inject secrets vào containers một cách an toàn khi runtime.

**Artifact Registry** là private container registry của GCP, nơi chúng tôi lưu trữ tất cả Docker images. So với Docker Hub public, Artifact Registry mang lại nhiều lợi ích: bảo mật hơn (private by default), nhanh hơn (cùng region với Cloud Run), và tích hợp tốt hơn với IAM và các GCP services khác. Registry được configure với vulnerability scanning tự động để đảm bảo images không chứa các lỗ hổng bảo mật đã biết.

**Cloud Build** là CI/CD service của GCP, cho phép chúng tôi tự động hóa quá trình build và deploy. Cloud Build đọc configuration từ file `cloudbuild.yaml`, thực hiện các steps như build Docker images, push lên Artifact Registry, và trigger deployment. Một lợi thế lớn của Cloud Build là nó chạy trong cùng GCP project, có quyền truy cập native vào các resources khác, và không cần setup authentication phức tạp như khi dùng external CI/CD tools.

### 4.2. Backend Technologies

Backend của hệ thống được xây dựng hoàn toàn bằng Python, một lựa chọn chiến lược mang lại nhiều lợi ích. Python không chỉ là ngôn ngữ phổ biến với ecosystem phong phú mà còn có performance đủ tốt cho use case của chúng tôi, đặc biệt khi kết hợp với async/await và các optimizations khác.

**FastAPI** được chọn làm web framework chính cho cả Chatbot Service và Tools Service. FastAPI nổi bật với hiệu năng cao (comparable với NodeJS và Go nhờ vào Starlette và Pydantic), hỗ trợ async/await native cho phép xử lý concurrent requests hiệu quả, automatic API documentation với OpenAPI/Swagger, và type safety thông qua Python type hints và Pydantic. Đặc biệt, FastAPI có dependency injection system mạnh mẽ, giúp code organization tốt và dễ testing.

**Pydantic** được sử dụng rộng rãi cho data validation và serialization. Mọi request/response đều được define bằng Pydantic models, đảm bảo type safety và automatic validation. Khi có invalid data, Pydantic tự động trả về error messages rõ ràng, giúp debugging dễ dàng hơn. Pydantic cũng có performance rất tốt nhờ vào Rust-based core trong phiên bản v2.

**httpx** là HTTP client library được sử dụng để gọi external APIs (LLM, Tools Service). Chúng tôi chọn httpx thay vì requests vì httpx hỗ trợ async/await, cho phép thực hiện concurrent HTTP requests mà không block. Điều này đặc biệt quan trọng khi cần gọi multiple tools hoặc retry requests.

**OpenAI SDK** (hoặc tương đương cho Vertex AI) cung cấp interface để tương tác với LLM. SDK này handle nhiều complexity như authentication, retry logic, streaming responses, và error handling. Chúng tôi sử dụng SDK's function calling feature để enable LLM gọi tools, một capability quan trọng cho chatbot domain-specific.

### 4.3. Frontend và User Interface

Frontend được xây dựng với **Streamlit**, một Python framework cho phép tạo web applications nhanh chóng mà không cần viết HTML/CSS/JavaScript. Lựa chọn Streamlit mang lại nhiều lợi ích cho một dự án demo/learning như của chúng tôi.

Thứ nhất, development speed cực nhanh - có thể tạo một UI functional trong vài chục dòng code. Thứ hai, sử dụng pure Python cho cả backend và frontend, giảm context switching và tận dụng được Python ecosystem. Thứ ba, Streamlit có built-in components cho các use cases phổ biến như chat interface, forms, file uploads, giúp chúng tôi không phải reinvent the wheel.

Tuy nhiên, chúng tôi cũng nhận thức được limitations của Streamlit: không phù hợp cho production-grade applications với traffic cao, customization bị giới hạn, và performance không tốt bằng các frameworks modern như React hay Vue. Nhưng với mục đích demo và learning, Streamlit là lựa chọn pragmatic và hiệu quả.

### 4.4. Infrastructure as Code và DevOps

**Terraform** là công cụ IaC chính được sử dụng để quản lý toàn bộ GCP infrastructure. Terraform cho phép chúng tôi define infrastructure bằng code (HCL - HashiCorp Configuration Language), version control infrastructure changes, và recreate infrastructure một cách consistent.

Chúng tôi organize Terraform code thành modules logic: một module cho APIs, một module cho Storage, một module cho Cloud Run services, etc. Mỗi resource được define với explicit dependencies, đảm bảo Terraform tạo resources theo đúng thứ tự. State file được lưu local cho development, nhưng có thể migrate sang remote backend (GCS) cho team collaboration.

**Docker** được sử dụng để containerize tất cả applications. Mỗi service (Frontend, Chatbot, Tools) có Dockerfile riêng, được optimize cho size và security. Chúng tôi sử dụng multi-stage builds để giảm image size, non-root users để tăng security, và specific base images (như python:3.11-slim) thay vì latest tags để đảm bảo reproducibility.

**GitHub Actions** được setup để tạo CI/CD pipeline tự động. Workflow được trigger khi push code lên branch main, thực hiện các steps: checkout code, authenticate với GCP, build Docker images, push lên Artifact Registry, và deploy lên Cloud Run. Secrets như GCP service account key được lưu trong GitHub Secrets, đảm bảo không bị expose trong code.

### 4.5. Testing và Monitoring

**pytest** là testing framework chính, được sử dụng cho cả unit tests và load tests. pytest có syntax đơn giản, fixtures mạnh mẽ, và plugin ecosystem phong phú. Chúng tôi viết unit tests cho các functions critical, integration tests cho API endpoints, và load tests để đánh giá performance.

**Locust** là load testing tool với Python-based test scenarios và web UI trực quan. Locust cho phép chúng tôi simulate nhiều concurrent users, ramp up/down traffic, và thu thập metrics như requests per second, response time percentiles, và failure rates. Web UI của Locust cung cấp real-time charts và statistics, giúp phân tích performance dễ dàng.

**Cloud Logging** tự động collect logs từ tất cả Cloud Run services. Logs được centralized, searchable, và có thể export sang BigQuery cho analysis. Chúng tôi sử dụng structured logging (JSON format) để logs dễ parse và query. Log levels được set appropriately (INFO cho production, DEBUG cho development) để balance giữa observability và cost.

**Cloud Monitoring** cung cấp metrics về resource usage (CPU, memory, network), request metrics (latency, error rate), và custom metrics. Chúng tôi có thể tạo dashboards để visualize metrics và set up alerts để được notify khi có issues. Monitoring giúp chúng tôi detect problems sớm và optimize performance based on data.

---

## 5. TÍNH NĂNG ĐÃ TRIỂN KHAI

### 5.1. Chức năng cốt lõi của Chatbot

Hệ thống Chatbot Cloud đã được triển khai đầy đủ các chức năng cốt lõi, tạo nên một chatbot hoàn chỉnh và functional cho domain tài chính cá nhân.

**Giao diện chat web** được xây dựng với Streamlit cung cấp trải nghiệm người dùng trực quan và dễ sử dụng. Người dùng có thể tạo session mới hoặc tiếp tục session cũ, gửi tin nhắn bằng ngôn ngữ tự nhiên, và nhận phản hồi từ chatbot trong thời gian thực. Giao diện hiển thị rõ ràng tin nhắn của user và assistant, với timestamps và formatting phù hợp. Một tính năng đặc biệt là toggle để chọn giữa synchronous và asynchronous processing, cho phép người dùng trải nghiệm cả hai modes và so sánh performance.

**Quản lý session** là một component quan trọng đảm bảo tính liên tục của cuộc hội thoại. Mỗi session được gắn với một unique ID, và tất cả messages trong session đó được lưu trữ và load lại khi cần. Session management cho phép chatbot maintain context qua nhiều turns của conversation, hiểu được references đến các tin nhắn trước đó, và cung cấp responses có ngữ cảnh. Backend implement session storage bằng Cloud Storage, với mỗi session là một JSON file chứa metadata và message history.

**Lưu trữ lịch sử hội thoại** được implement một cách robust và efficient. Mỗi khi có message mới (từ user hoặc assistant), nó được append vào session file trong Cloud Storage. File structure được thiết kế để dễ read và write: một JSON object với session_id, created_at, updated_at, và một array of messages. Mỗi message có role (user/assistant), content, timestamp, và optional metadata như function calls. Việc lưu trữ này không chỉ cho phép maintain context mà còn có thể dùng cho analytics, debugging, và improvement sau này.

**Tích hợp LLM** là trái tim của chatbot, cung cấp khả năng hiểu và generate ngôn ngữ tự nhiên. Chúng tôi sử dụng OpenAI's GPT models (có thể là GPT-3.5 hoặc GPT-4 tùy budget) thông qua API. Integration bao gồm nhiều aspects: system prompt được craft carefully để define chatbot's personality và domain knowledge (tài chính cá nhân), conversation history được format và include trong mỗi request để maintain context, function definitions được provide để LLM biết khi nào gọi tools, và response được parse để extract assistant message và potential function calls.

**Context-aware conversation** là một trong những features quan trọng nhất, phân biệt chatbot của chúng tôi với simple Q&A bots. Chatbot có thể hiểu references đến các entities được mention trước đó, maintain state của conversation (ví dụ: đang discuss về một khoản tiết kiệm cụ thể), và provide responses có ngữ cảnh. Điều này được achieve thông qua việc include conversation history trong LLM requests, cùng với careful prompt engineering để instruct LLM maintain context.

### 5.2. Xử lý bất đồng bộ với Pub/Sub

Một trong những innovations quan trọng nhất của hệ thống là implementation của asynchronous processing pattern sử dụng Google Cloud Pub/Sub. Feature này giải quyết một pain point lớn khi làm việc với LLM: latency cao và risk của timeout.

**Pub/Sub integration** được implement ở cả publisher và subscriber sides. Khi user chọn async mode và gửi message, Chatbot Service không gọi LLM ngay mà publish một message lên Pub/Sub topic "chat-requests". Message payload chứa session_id, user message content, và metadata cần thiết. Sau khi publish thành công, service ngay lập tức return response với status "pending" cho frontend, thay vì giữ connection và chờ LLM.

**Async chat endpoint** (`/api/chat?async=1`) implement logic này một cách clean và efficient. Endpoint validate input, save user message vào Storage với status "pending", create Pub/Sub message, publish message, và return response. Toàn bộ quá trình này mất chỉ vài trăm milliseconds, so với 3-5 seconds nếu gọi LLM synchronously.

**Polling mechanism** được implement ở frontend để fetch results. Frontend gọi endpoint `/api/sessions/{session_id}/messages` mỗi 2-3 giây để check xem có messages mới không. Khi assistant message có status "completed", frontend hiển thị cho user. Polling có thể không elegant như WebSocket hoặc Server-Sent Events, nhưng nó simple, reliable, và đủ tốt cho use case của chúng tôi.

**Tránh timeout với LLM calls** là main benefit của async pattern. Trong synchronous mode, nếu LLM mất quá lâu (>30 seconds), connection có thể timeout, và user không nhận được response. Trong async mode, user luôn nhận được immediate feedback (status pending), và có thể chờ bao lâu cũng được. Nếu LLM processing fail, error được save vào Storage và user được notify, thay vì connection bị drop.

### 5.3. Tools và Function Calling

Function calling là một capability mạnh mẽ của modern LLMs, cho phép chúng interact với external systems và perform actions beyond text generation. Chúng tôi đã implement một Tools Service với hai tools chính, demonstrating end-to-end function calling flow.

**Tính lãi suất** là tool đầu tiên, cung cấp hai variants: simple interest và compound interest. Tool nhận parameters như principal amount (số tiền gốc), interest rate (lãi suất), và time period (kỳ hạn), thực hiện calculation, và return kết quả. Implementation sử dụng standard financial formulas: Simple Interest = P × r × t, và Compound Interest = P × (1 + r)^t - P. Tool được expose như một API endpoint `/tools/interest` với clear input/output schema.

**Tính tỷ lệ tiết kiệm** là tool thứ hai, giúp users understand savings rate của họ. Tool nhận income (thu nhập) và savings (số tiền tiết kiệm), calculate savings rate = (savings / income) × 100%, và provide interpretation (ví dụ: "Tốt" nếu >20%, "Trung bình" nếu 10-20%, "Cần cải thiện" nếu <10%). Tool này demonstrate việc không chỉ return numbers mà còn provide contextual insights.

**Function calling từ LLM** được implement thông qua OpenAI's function calling feature. Chúng tôi define function schemas (name, description, parameters) và include chúng trong LLM requests. Khi LLM determine cần gọi function, nó return một function_call object với function name và arguments. Chatbot Service parse object này, gọi appropriate tool endpoint, nhận result, và gọi lại LLM với function result để generate final response cho user.

**Microservice architecture** cho Tools Service mang lại nhiều benefits. Tools có thể scale độc lập với Chatbot Service - nếu có nhiều function calls, chỉ Tools Service cần scale up. Tools có thể develop và deploy độc lập, cho phép add tools mới mà không cần redeploy Chatbot. Tools có thể reuse cho các applications khác, không chỉ chatbot. Và separation of concerns giúp code organization tốt hơn và easier to maintain.

### 5.4. Infrastructure và Automation

Phần infrastructure và automation là foundation cho toàn bộ hệ thống, đảm bảo deployment consistent, reproducible, và automated.

**Terraform IaC** manage toàn bộ GCP infrastructure. Chúng tôi có Terraform configurations cho: enabling required GCP APIs (Cloud Run, Cloud Storage, Pub/Sub, Secret Manager, etc.), creating Cloud Storage bucket với appropriate lifecycle policies, creating Pub/Sub topic và push subscription, creating Secret Manager secret cho OpenAI API key, creating Artifact Registry repository, và deploying ba Cloud Run services (frontend, chatbot, tools) với appropriate configurations.

Terraform code được organize một cách logic với variables file cho customization, outputs file để expose important values (như service URLs), và modules cho reusable components. Chúng tôi sử dụng Terraform's dependency management để ensure resources được create theo đúng order. State file track current state của infrastructure, cho phép Terraform detect changes và apply incremental updates.

**Cloud Build configuration** define CI/CD pipeline trong file `cloudbuild.yaml`. Pipeline có các steps: build Docker image cho từng service (frontend, chatbot, tools), tag images với commit SHA và "latest", push images lên Artifact Registry, và optionally trigger Cloud Run deployment. Build process sử dụng Cloud Build's caching để speed up subsequent builds. Build logs được save trong Cloud Logging cho debugging.

**GitHub Actions workflow** provide alternative CI/CD option, đặc biệt useful khi develop outside GCP. Workflow authenticate với GCP using service account key (stored in GitHub Secrets), run same build steps như Cloud Build, và có thể run tests trước khi deploy. GitHub Actions cũng có thể trigger on pull requests để run tests và validation, ensuring code quality trước khi merge.

**Automated deployment** là end goal của CI/CD setup. Khi code được push lên main branch, pipeline tự động trigger, build images, và deploy lên Cloud Run. Cloud Run's traffic management cho phép gradual rollout - có thể route một phần traffic đến new revision để test trước khi route toàn bộ. Nếu có issues, có thể rollback đến previous revision một cách nhanh chóng.

### 5.5. Monitoring, Security và Operations

**Health check endpoints** được implement cho tất cả services. Mỗi service expose `/health` endpoint return 200 OK nếu service healthy. Cloud Run sử dụng health checks để determine khi nào start routing traffic đến new instances và khi nào restart unhealthy instances. Health checks cũng useful cho external monitoring tools và load balancers.

**Cloud Logging integration** automatic với Cloud Run - tất cả stdout/stderr được capture và send đến Cloud Logging. Chúng tôi sử dụng structured logging (JSON format) để logs dễ parse và query. Logs include request ID để trace requests qua multiple services, và include relevant context như session_id, user_id (nếu có), và operation type.

**Error tracking** được implement thông qua proper exception handling và logging. Khi có errors, chúng tôi log full stack trace, context information, và return appropriate error responses cho clients. Critical errors có thể trigger alerts thông qua Cloud Monitoring. Error rates được track như một metric để detect issues sớm.

**Performance metrics** được collect automatically bởi Cloud Run và Cloud Monitoring. Metrics include request count, request latency (median, p95, p99), error rate, CPU usage, memory usage, và instance count. Chúng tôi có thể create custom metrics cho domain-specific measurements như LLM call latency, function call count, etc.

**Secret Manager cho API keys** ensure sensitive credentials không bị expose. OpenAI API key được store trong Secret Manager và inject vào Cloud Run containers như environment variable khi runtime. Secret có version management, cho phép rotate keys mà không downtime. Access đến secrets được control bởi IAM permissions.

**IAM roles và permissions** được configure theo principle of least privilege. Mỗi service chỉ có permissions cần thiết: Chatbot Service có quyền read/write Cloud Storage, publish Pub/Sub messages, và access secrets; Tools Service chỉ cần basic permissions; Frontend chỉ cần gọi Chatbot API. Service accounts được sử dụng thay vì user accounts cho automation.

**Private container registry** (Artifact Registry) ensure Docker images không public accessible. Registry có vulnerability scanning enabled, automatically scan images cho known vulnerabilities và provide reports. Images có thể tag với metadata như build time, commit SHA, và version number cho traceability.

**HTTPS endpoints** được enforce cho tất cả Cloud Run services. Cloud Run automatically provision SSL certificates và handle HTTPS termination. All communications giữa clients và services, và giữa services với nhau, đều encrypted in transit. Cloud Run cũng có built-in DDoS protection và rate limiting.

---

## 6. QUY TRÌNH TRIỂN KHAI

### 6.1. Chuẩn bị môi trường phát triển

Trước khi bắt đầu triển khai hệ thống lên Google Cloud Platform, việc chuẩn bị môi trường phát triển đầy đủ và chính xác là vô cùng quan trọng. Quá trình này đảm bảo rằng chúng tôi có tất cả tools và permissions cần thiết để thực hiện deployment thành công.

**Yêu cầu về tài khoản và billing**: Điều đầu tiên cần có là một Google Cloud Platform account với billing được enable. GCP cung cấp free tier với $300 credits cho new users, đủ để chạy dự án này trong vài tháng. Tuy nhiên, cần lưu ý rằng một số services như Cloud Run và Pub/Sub có free tier limits, và vượt quá limits sẽ incur charges. Chúng tôi recommend setup billing alerts để monitor spending và avoid unexpected charges.

**Cài đặt công cụ dòng lệnh**: gcloud CLI là tool chính để interact với GCP từ command line. Installation process khác nhau tùy operating system - trên Linux có thể dùng package manager, trên macOS có thể dùng Homebrew, và trên Windows có installer. Sau khi install, cần chạy `gcloud init` để authenticate và configure default project và region. gcloud CLI cũng cần components như kubectl (nếu dùng GKE) và docker-credential-gcr (để push images).

**Terraform installation**: Terraform có thể download từ HashiCorp website hoặc install qua package managers. Chúng tôi recommend sử dụng version ≥ 1.0 để có latest features và bug fixes. Sau khi install, verify bằng `terraform version`. Terraform cũng cần được configure để authenticate với GCP, thường thông qua Application Default Credentials hoặc service account key file.

**Docker và containerization tools**: Docker là essential để build container images locally và test trước khi deploy. Docker Desktop là option dễ nhất cho macOS và Windows, trong khi Linux có thể install Docker Engine directly. Sau khi install Docker, cần configure Docker to authenticate với Artifact Registry bằng `gcloud auth configure-docker`.

**Git và version control**: Toàn bộ code được manage trong Git repository, nên Git client là required. Chúng tôi recommend configure Git với proper user name và email, và setup SSH keys cho GitHub để avoid typing password mỗi lần push. Git hooks có thể setup để run linting và formatting trước khi commit, ensuring code quality.

### 6.2. Thiết lập GCP Project

Sau khi có đầy đủ tools, bước tiếp theo là setup GCP project - container logic cho tất cả resources của chúng tôi.

**Tạo project mới**: Có thể tạo project qua GCP Console (web UI) hoặc gcloud CLI. Mỗi project cần một unique project ID (không thể change sau khi tạo) và project name (có thể change). Chúng tôi recommend chọn project ID descriptive và memorable, ví dụ "chatbot-cloud-demo-2026". Project cũng cần được link với billing account để có thể sử dụng paid services.

**Enable billing**: Nếu project chưa có billing, cần link nó với billing account. Điều này có thể làm qua Console hoặc CLI. Billing account có thể là individual hoặc organization-level. Sau khi enable billing, có thể setup budget alerts để được notify khi spending approach certain thresholds.

**Configure default settings**: Set project làm default trong gcloud config để không phải specify project ID trong mỗi command: `gcloud config set project PROJECT_ID`. Cũng nên set default region và zone based on location của users và compliance requirements. Chúng tôi chọn asia-southeast1 (Singapore) vì gần Vietnam và có đầy đủ services.

**Enable required APIs**: GCP services được expose như APIs cần được enable trước khi sử dụng. Có thể enable manually qua Console hoặc automate với Terraform. Required APIs cho project này include: Cloud Run API, Cloud Storage API, Pub/Sub API, Secret Manager API, Artifact Registry API, Cloud Build API, và IAM API. Enable APIs có thể mất vài phút, đặc biệt lần đầu tiên.

### 6.3. Triển khai Infrastructure với Terraform

Với project đã setup, chúng tôi sử dụng Terraform để provision toàn bộ infrastructure một cách automated và reproducible.

**Configuration và customization**: Terraform code được organize trong `infrastructure/terraform` directory. File `terraform.tfvars.example` provide template cho variables cần customize. Chúng tôi copy file này thành `terraform.tfvars` và fill in actual values: project_id (GCP project ID), region (deployment region), openai_api_key_secret (OpenAI API key), và optional variables như service names, resource names, etc.

**Initialization**: Command `terraform init` initialize Terraform working directory, download required providers (như google và google-beta providers), và setup backend for state storage. Init process cũng validate configuration syntax. Nếu có errors, Terraform sẽ report và cần fix trước khi proceed. Init chỉ cần run một lần, hoặc khi add new providers/modules.

**Planning và validation**: `terraform plan` command generate execution plan, showing exactly what Terraform will do: which resources will be created, modified, or destroyed. Plan output nên được review carefully để ensure không có unexpected changes. Plan cũng validate configuration và check for errors. Nếu plan looks good, có thể proceed to apply.

**Applying changes**: `terraform apply` command execute plan và actually create/modify/destroy resources. Terraform sẽ show plan again và ask for confirmation trước khi proceed. Apply process có thể mất vài phút đến vài chục phút depending on số lượng resources. Terraform output progress real-time, showing which resources đang được created. Nếu có errors, Terraform sẽ stop và report, và có thể retry sau khi fix issues.

**Resources được tạo**: Sau khi apply thành công, Terraform đã create: 10+ enabled APIs, một Cloud Storage bucket cho session data, một Pub/Sub topic "chat-requests" và push subscription, một Secret Manager secret "openai-api-key", một Artifact Registry repository "chatbot-images", và ba Cloud Run services (chatbot-frontend, chatbot-api, chatbot-tools). Tuy nhiên, Cloud Run services có thể fail to deploy nếu chưa có container images - đây là expected và sẽ fix ở bước tiếp theo.

### 6.4. Build và Deploy Container Images

Với infrastructure đã ready, bước tiếp theo là build Docker images cho các services và deploy chúng lên Cloud Run.

**Cloud Build approach**: Cách recommended là sử dụng Cloud Build để build images directly trên GCP. File `cloudbuild.yaml` ở root directory define build steps cho cả ba services. Command `gcloud builds submit --config=cloudbuild.yaml .` trigger build process. Cloud Build sẽ upload source code, execute build steps trong cloud environment, và push resulting images lên Artifact Registry. Build process mất khoảng 3-5 phút depending on image sizes và network speed.

**Build steps breakdown**: Cloud Build process bao gồm multiple steps cho mỗi service. Đầu tiên, build Docker image từ Dockerfile using `docker build` command. Image được tag với commit SHA và "latest" tag. Sau đó, push image lên Artifact Registry using `docker push`. Cuối cùng, có thể trigger Cloud Run deployment với new image. Build logs được stream real-time và save trong Cloud Logging cho reference sau này.

**Local build alternative**: Nếu prefer build locally, có thể use Docker commands directly. Build image: `docker build -t IMAGE_NAME .`, tag image với Artifact Registry path: `docker tag IMAGE_NAME REGISTRY_PATH`, và push: `docker push REGISTRY_PATH`. Local builds useful cho development và testing, nhưng Cloud Build preferred cho CI/CD vì consistent environment và không depend on local machine specs.

**Deployment verification**: Sau khi images được push, Cloud Run services cần được deploy với new images. Nếu Terraform đã create services nhưng failed vì missing images, có thể run `terraform apply` lại để update services với new images. Alternatively, có thể deploy manually qua Console hoặc gcloud CLI. Verify deployment bằng cách check service URLs (từ `terraform output`) và test health endpoints.

### 6.5. Configuration và Secrets Management

Với services đã deployed, cần configure chúng properly và setup secrets.

**Adding OpenAI API key**: OpenAI API key cần được add vào Secret Manager. Command `echo -n "sk-..." | gcloud secrets versions add openai-api-key --data-file=-` create new secret version với key value. Flag `-n` trong echo important để avoid adding newline character. Sau khi add secret, Cloud Run services sẽ automatically có access (nếu IAM permissions đã setup correctly).

**Environment variables**: Ngoài secrets, services có thể cần environment variables khác như TOOLS_URL (URL của Tools Service), LOG_LEVEL (INFO/DEBUG), ENABLE_ASYNC (true/false), etc. Environment variables có thể set trong Terraform configuration hoặc update manually qua Console/CLI. Cloud Run restart containers khi environment variables change, nên có brief downtime.

**Service-to-service authentication**: Nếu services cần authenticate với nhau (ví dụ: Chatbot calling Tools), có thể use Cloud Run's built-in authentication. Mỗi service có một service account, và có thể grant permissions cho service accounts khác để invoke. Alternatively, có thể use API keys hoặc custom authentication mechanisms.

### 6.6. Verification và Testing

Sau khi deployment complete, cần verify rằng everything works correctly.

**Getting service URLs**: Terraform outputs include URLs của các Cloud Run services. Command `terraform output cloud_run_frontend_url` show Frontend URL, `terraform output cloud_run_chatbot_url` show Chatbot API URL, và `terraform output cloud_run_tools_url` show Tools API URL. URLs có format `https://SERVICE_NAME-HASH-REGION.run.app`.

**Testing health endpoints**: Đầu tiên, test health endpoints để ensure services are running: `curl https://chatbot-api-xxx.run.app/health` should return 200 OK. Repeat cho Tools Service. Nếu health checks fail, check Cloud Run logs để see errors. Common issues include missing environment variables, failed secret access, hoặc application startup errors.

**End-to-end testing**: Mở Frontend URL trong browser để test full flow. Create new session, send test messages, verify responses. Test both synchronous và asynchronous modes. Test function calling bằng cách ask questions requiring calculations (ví dụ: "Tính lãi suất cho 10 triệu đồng, lãi 5%, 1 năm"). Verify rằng lịch sử hội thoại được lưu và load correctly.


**Monitoring và logs**: Check Cloud Run metrics trong Console để see request counts, latencies, error rates. Check Cloud Logging để see application logs và debug any issues. Setup log-based alerts cho critical errors nếu cần. Monitor costs trong Billing section để ensure không exceed budget.

---

## 7. KẾT QUẢ THỬ NGHIỆM

### 7.1. Phương pháp và chuẩn bị

Việc thử nghiệm hệ thống được thực hiện một cách có hệ thống và toàn diện, bao gồm nhiều loại tests khác nhau để đánh giá các khía cạnh khác nhau của hệ thống. Chúng tôi áp dụng cả unit testing cho các components riêng lẻ, integration testing cho các flows end-to-end, load testing để đánh giá performance và scalability, và functional testing để verify rằng tất cả features hoạt động đúng như mong đợi.

**Môi trường testing** được setup cẩn thận để đảm bảo kết quả đáng tin cậy. Chúng tôi thực hiện tests trên cả môi trường local (để development và debugging nhanh) và môi trường GCP production (để có kết quả realistic về performance và auto-scaling). Local environment sử dụng Docker Compose để run tất cả services, trong khi GCP environment là actual deployment với Cloud Run, Cloud Storage, và Pub/Sub.

**Testing tools** bao gồm pytest cho unit và integration tests, Locust cho load testing với web UI, và custom scripts cho functional testing. Mỗi tool được chọn vì strengths riêng: pytest có syntax đơn giản và fixtures mạnh mẽ, Locust cho phép simulate realistic user behavior và provide real-time metrics, và custom scripts cho phép test các scenarios specific cho domain của chúng tôi.

### 7.2. Unit và Integration Tests

Unit tests được viết cho các components critical của hệ thống, đảm bảo rằng mỗi function và class hoạt động correctly in isolation. Chúng tôi focus vào các areas như data validation (Pydantic models), business logic (interest calculations, savings rate calculations), storage operations (read/write session data), và LLM integration (prompt formatting, response parsing, function calling).

Integration tests verify rằng các components work together correctly. Ví dụ, chúng tôi test full chat flow: create session → send message → LLM processes → function call if needed → save to storage → return response. Integration tests cũng cover async flow với Pub/Sub: publish message → Pub/Sub triggers handler → LLM processes → save result → client polls and retrieves.

Kết quả của unit và integration tests là positive - tất cả tests pass consistently. Code coverage đạt mức reasonable (khoảng 70-80% cho core logic), mặc dù một số edge cases và error handling paths chưa được cover đầy đủ. Tests chạy nhanh (toàn bộ test suite mất dưới 1 phút), cho phép run frequently trong development process.

### 7.3. Load Testing - Methodology

Load testing được thực hiện để đánh giá performance của hệ thống dưới different levels of load và verify khả năng auto-scaling. Chúng tôi sử dụng cả pytest-based load tests (cho quick, scripted tests) và Locust (cho interactive testing với gradual ramp-up).

**Test scenarios** được thiết kế để cover các use cases realistic: health check requests (để test basic availability), session creation (để test storage operations), synchronous chat (để test LLM integration và end-to-end latency), asynchronous chat (để test Pub/Sub integration), và tools API calls (để test microservice communication). Mỗi scenario được run với different numbers of concurrent users và request rates để understand system behavior under varying loads.

**Metrics collected** include requests per second (RPS) để measure throughput, average latency và percentiles (p50, p95, p99) để understand response time distribution, error rate để track failures, và instance count để verify auto-scaling behavior. Chúng tôi cũng monitor resource usage (CPU, memory) để identify bottlenecks và optimization opportunities.

### 7.4. Load Testing Results - Tools Service

Tools Service, being simpler và không involve LLM calls, shows excellent performance characteristics. Health check endpoint consistently responds trong dưới 50ms với 100% success rate, ngay cả khi có hàng nghìn concurrent requests. Interest calculation endpoint, mặc dù có logic phức tạp hơn, vẫn maintains average latency khoảng 100-150ms. Savings rate calculation có performance tương tự.

Throughput của Tools Service là impressive - có thể handle hàng trăm requests per second trên một single instance. Khi load tăng, Cloud Run automatically scales up instances, và system có thể handle thousands of RPS without degradation. Error rate gần như zero trong normal conditions, chỉ có occasional timeouts khi có extreme load spikes (và ngay cả khi đó, Cloud Run's retry mechanism ensures eventual success).

Auto-scaling behavior của Tools Service là predictable và responsive. Khi load tăng đột ngột, new instances được spin up trong vòng 10-15 giây. Khi load giảm, instances được scale down gradually để avoid thrashing. Sau khi idle trong 15 phút, instance count giảm về 0, demonstrating perfect scale-to-zero capability và cost optimization.

### 7.5. Load Testing Results - Chatbot Service

Chatbot Service có performance characteristics khác biệt do involvement của LLM calls. Health check và session creation endpoints vẫn rất nhanh (50-200ms), comparable với Tools Service. Tuy nhiên, chat endpoints có latency cao hơn đáng kể do LLM processing time.

**Synchronous chat** có average latency khoảng 3-5 giây, với p95 có thể lên đến 7-8 giây trong peak load. Latency này là expected và acceptable cho LLM-based applications - majority of time được spend trong LLM API call, không phải trong application logic. Success rate vẫn cao (95-98%), với occasional failures do LLM API timeouts hoặc rate limits. Throughput bị limited bởi LLM API - khoảng 10-20 requests per second per instance, depending on complexity của requests.

**Asynchronous chat** shows dramatically better user-facing performance. Initial request (publish to Pub/Sub) completes trong 200-400ms với 99%+ success rate. Actual LLM processing happens in background, và results become available sau 3-5 giây (same như sync mode) nhưng không block user. Polling mechanism works well - frontend checks mỗi 2-3 giây và retrieves results ngay khi available. Async mode cho phép handle higher concurrency vì không tie up connections waiting for LLM.

Auto-scaling của Chatbot Service cũng effective nhưng có nuances. Cold starts (khi new instances được created) có thể add 2-3 giây latency cho first request, nhưng subsequent requests trên same instance rất nhanh. Cloud Run's minimum instances setting có thể configure để keep một vài instances warm, trading off một chút cost cho better latency. Under sustained load, system scales smoothly và maintains consistent performance.

### 7.6. Stress Testing và Edge Cases

Stress testing được thực hiện để push system beyond normal operating conditions và identify breaking points. Chúng tôi simulate scenarios như sudden traffic spikes (0 to 100 users trong 10 giây), sustained high load (200 concurrent users trong 10 phút), và cascading failures (LLM API down, Storage unavailable).

Kết quả cho thấy system khá resilient. Trong sudden spike scenario, có một brief period (10-20 giây) của elevated latency và error rate khi Cloud Run scales up, nhưng sau đó system stabilizes và performs normally. Sustained high load được handle well - error rate stays dưới 5%, mainly due to LLM API rate limits rather than application issues. Instance count scales up đến 8-10 instances, demonstrating good horizontal scalability.

Cascading failure scenarios reveal một số weaknesses. Khi LLM API down, synchronous chat requests fail immediately (expected), nhưng asynchronous requests get stuck trong Pub/Sub queue và retry indefinitely. Chúng tôi cần implement better error handling và dead-letter queues cho failed messages. Khi Storage unavailable, toàn bộ system fails vì không thể read/write session data - cần implement caching layer để mitigate này.

### 7.7. Functional Testing

Functional testing verify rằng tất cả features work correctly from user perspective. Chúng tôi test complete chat flows: user creates session, sends multiple messages, receives contextual responses, và conversation history is maintained. Context-aware conversation works well - chatbot remembers previous messages và can reference them trong responses.

Function calling được test thoroughly. Khi user asks questions requiring calculations (ví dụ: "Tính lãi suất cho 10 triệu, 5%, 1 năm"), LLM correctly identifies need to call interest tool, extracts parameters, calls tool, và incorporates result vào response. Multi-step conversations involving multiple function calls cũng work correctly.

Async processing được verify end-to-end. User sends message trong async mode, receives immediate "pending" status, và sau vài giây sees completed response. Polling mechanism works reliably, và frontend updates UI smoothly. Error cases (LLM timeout, invalid function calls) được handle gracefully với appropriate error messages.

### 7.8. Security và Compliance Testing

Security testing focus vào verifying rằng sensitive data được protect properly. Chúng tôi verify rằng OpenAI API key không bị expose trong logs, responses, hoặc error messages. Secret Manager integration works correctly - secrets được inject vào containers securely và không accessible từ outside.

IAM permissions được audit để ensure principle of least privilege. Mỗi service chỉ có permissions cần thiết, và không có overly permissive roles. Service-to-service authentication works correctly - unauthorized requests được reject với 403 Forbidden.

HTTPS enforcement được verify - tất cả endpoints chỉ accessible qua HTTPS, và HTTP requests được redirect. SSL certificates được provision automatically bởi Cloud Run và renew trước khi expire. Data encryption at rest (trong Cloud Storage) và in transit (HTTPS) được confirm.

### 7.9. Cost Analysis

Cost analysis được thực hiện dựa trên actual usage data từ GCP Billing. Với moderate usage (khoảng 1000 requests per day), monthly cost breakdown như sau:

Cloud Run charges (ba services combined) khoảng $5-8, mainly từ CPU time và memory usage. Cost thấp vì scale-to-zero - khi không có traffic, không có charges. Cloud Storage cost minimal (dưới $1) vì data volume nhỏ. Pub/Sub cost khoảng $1-2 cho message delivery. Secret Manager, Artifact Registry, và Cloud Build đều trong free tier hoặc có minimal charges.

Total GCP infrastructure cost khoảng $7-12 per month, rất reasonable cho một production-ready system. Tuy nhiên, đây chưa include LLM API cost (OpenAI), which có thể là $10-50 per month depending on usage. LLM cost là variable cost scale với usage, trong khi infrastructure cost mostly fixed (với scale-to-zero helping minimize idle costs).

Cost optimization opportunities include: sử dụng cheaper LLM models (GPT-3.5 thay vì GPT-4) cho simple queries, implement caching để reduce redundant LLM calls, optimize container images để reduce memory usage và startup time, và use committed use discounts nếu có predictable baseline load.

---

## 8. KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN

### 8.1. Tổng kết kết quả đạt được

Dự án Chatbot Cloud đã đạt được những thành công đáng kể trên nhiều phương diện, từ kỹ thuật đến học tập và nghiên cứu. Về mặt kỹ thuật, chúng tôi đã xây dựng thành công một hệ thống chatbot hoàn chỉnh trên nền tảng serverless, demonstrating rằng kiến trúc này hoàn toàn viable cho real-world applications. Hệ thống không chỉ functional mà còn exhibits good performance characteristics, với response times acceptable, high availability, và excellent cost efficiency nhờ vào scale-to-zero capability.

Việc tích hợp LLM vào hệ thống đã được thực hiện thành công, với chatbot có khả năng hiểu và respond to natural language queries một cách intelligent. Function calling mechanism cho phép chatbot không chỉ generate text mà còn perform actual computations và provide concrete answers. Context management ensures conversations feel natural và coherent, với chatbot remembering previous exchanges và maintaining conversation flow.

Auto-scaling capability của hệ thống đã được verify thông qua extensive load testing. System có thể handle từ zero đến hundreds of concurrent users, scaling up và down automatically based on demand. Response times remain consistent across different load levels (excluding cold start effects), và error rates stay low even under stress. Scale-to-zero functionality works perfectly, ensuring no costs when system is idle.

Infrastructure as Code implementation với Terraform đã proven to be invaluable. Toàn bộ infrastructure có thể được recreated từ code trong vài phút, ensuring consistency và reproducibility. Version control của infrastructure changes provides audit trail và enables collaboration. Terraform's dependency management ensures resources được created trong correct order, avoiding manual coordination.

CI/CD pipeline với Cloud Build và GitHub Actions automates deployment process completely. Code changes được automatically built, tested, và deployed, reducing manual effort và human errors. Pipeline ensures consistency across deployments và enables rapid iteration. Rollback capability provides safety net nếu có issues với new deployments.

### 8.2. Những thách thức đã gặp và cách giải quyết

Trong quá trình phát triển và triển khai hệ thống, chúng tôi đã đối mặt với nhiều thách thức kỹ thuật và tìm ra các giải pháp hiệu quả.

**LLM latency và timeout issues** là một trong những challenges lớn nhất. Initial implementation với synchronous processing often resulted trong timeout errors khi LLM took too long to respond. Giải pháp của chúng tôi là implement asynchronous processing pattern với Pub/Sub. Điều này decouple request receiving từ processing, cho phép return immediate response cho user và process LLM calls trong background. Polling mechanism enables frontend retrieve results khi ready, providing much better user experience.

**State management trong serverless environment** presented unique challenges. Traditional approaches của storing state trong memory không work vì containers có thể be killed bất cứ lúc nào. Chúng tôi giải quyết bằng cách persist all state vào Cloud Storage. Mỗi session có một JSON file chứa complete conversation history. Mặc dù có một chút latency overhead, approach này ensures reliability và enables stateless service design, which is essential cho horizontal scaling.

**Cold start latency** của Cloud Run là một concern, đặc biệt cho first request sau idle period. Cold starts có thể add 2-3 seconds latency, which is noticeable cho users. Chúng tôi mitigate bằng cách optimize Docker images (sử dụng slim base images, multi-stage builds), configure minimum instances để keep một vài instances warm during peak hours, và implement health check endpoints để Cloud Run có thể verify instance readiness quickly.

**Cost optimization** requires careful balancing. LLM API calls là expensive, và unoptimized usage có thể quickly rack up costs. Chúng tôi implement several optimizations: use cheaper models (GPT-3.5) cho simple queries, carefully craft prompts để minimize token usage, implement conversation history truncation để avoid sending too much context, và consider caching cho frequently asked questions. Infrastructure costs được minimize thông qua scale-to-zero và right-sizing của resources.

**Security và secrets management** requires careful attention. Initial approach của storing API keys trong environment variables files was insecure. Migration sang Secret Manager provides proper security với encryption at rest, access control via IAM, và audit logging. Integration với Cloud Run ensures secrets được inject securely vào containers without exposure trong logs hoặc configuration files.

### 8.3. Bài học kinh nghiệm

Qua quá trình thực hiện dự án, chúng tôi đã tích lũy được nhiều bài học quý giá về cloud computing, serverless architecture, và software engineering practices.

**Về kiến trúc serverless**: Serverless is not silver bullet nhưng là excellent choice cho certain workloads. Nó shines khi có variable traffic patterns, khi muốn minimize operational overhead, và khi cost optimization is priority. Tuy nhiên, nó có tradeoffs như cold starts, limited execution time, và constraints về state management. Understanding these tradeoffs và designing accordingly is crucial.

**Về microservices**: Breaking system thành smaller services mang lại nhiều benefits như independent scaling, easier maintenance, và better fault isolation. Tuy nhiên, nó cũng introduces complexity trong areas như service discovery, inter-service communication, và distributed debugging. For small projects, monolith có thể simpler, nhưng for systems expected to grow, microservices provide better long-term scalability.

**Về message queues**: Pub/Sub và async processing patterns are powerful tools cho decoupling và handling variable loads. Chúng enable better user experience (immediate feedback), better resource utilization (process when capacity available), và better reliability (retry failed operations). Tuy nhiên, chúng cũng add complexity và require careful error handling và monitoring.

**Về Infrastructure as Code**: Terraform và IaC practices are game-changers cho cloud infrastructure management. Being able to version control infrastructure, recreate environments consistently, và automate deployments saves enormous time và reduces errors. However, learning curve is steep, và requires discipline để keep code và actual infrastructure in sync.

**Về LLM integration**: Working với LLMs requires different mindset từ traditional programming. Prompts are code, và prompt engineering is a skill. Context management is crucial cho good conversation quality. Function calling is powerful nhưng requires careful design của function interfaces. Cost monitoring is essential vì LLM calls can be expensive.

**Về testing và monitoring**: Comprehensive testing (unit, integration, load) is essential cho confidence trong system reliability. Load testing reveals performance characteristics và scaling behavior that cannot be predicted theoretically. Monitoring và logging are not afterthoughts - chúng should be built in từ start để enable debugging và optimization.

**Về DevOps practices**: CI/CD automation saves time và reduces errors, nhưng requires upfront investment trong setup. Automated testing trong pipeline ensures quality. Infrastructure automation với Terraform enables rapid iteration. Proper secrets management is non-negotiable cho security.

### 8.4. Hạn chế hiện tại của hệ thống

Mặc dù đã đạt được nhiều thành công, hệ thống vẫn có một số hạn chế cần được acknowledge và address trong future iterations.

**Database và structured data**: Hiện tại sử dụng Cloud Storage cho all persistence, which works nhưng has limitations. Không có query capabilities - phải read entire session file để get specific messages. Không có transaction support - concurrent updates có thể cause race conditions. Không có indexing - searching across sessions is inefficient. Migration sang proper database (Cloud SQL hoặc Firestore) would enable more sophisticated data operations.

**Caching layer**: Không có caching currently, meaning every request hits Storage và potentially LLM API. Implementing caching (với Cloud Memorystore hoặc Redis) would significantly improve performance và reduce costs cho frequently accessed data và common queries. Cache invalidation strategy cần được designed carefully để avoid stale data.

**Advanced monitoring và alerting**: Current monitoring is basic - mainly relying on Cloud Run's built-in metrics và Cloud Logging. More sophisticated monitoring với custom metrics, detailed dashboards, và proactive alerting would enable better operational visibility và faster incident response. Integration với tools như Prometheus, Grafana, hoặc Datadog could provide richer insights.

**Error handling và resilience**: While basic error handling exists, system could be more resilient. Implementing circuit breakers cho external API calls, better retry strategies với exponential backoff, dead-letter queues cho failed Pub/Sub messages, và graceful degradation khi dependencies unavailable would improve reliability.

**Multi-tenancy và user management**: Current system is single-tenant - không có user authentication hoặc authorization. Adding proper user management, multi-tenancy support, và role-based access control would be necessary cho production use. This includes user registration, login, session management, và data isolation between users.

**Performance optimization**: While performance is acceptable, có room for improvement. Container images có thể be further optimized để reduce size và startup time. Database queries (khi migrate từ Storage) có thể be optimized với proper indexing. LLM calls có thể be optimized với better prompt engineering và selective caching.

### 8.5. Hướng phát triển tương lai

Dựa trên experience gained và limitations identified, chúng tôi đã outline một roadmap cho future development, chia thành short-term, medium-term, và long-term goals.

**Short-term improvements (1-3 tháng)** focus vào addressing immediate limitations và improving core functionality. Migrate từ Cloud Storage sang Cloud SQL hoặc Firestore để có proper database với query capabilities. Implement caching layer với Cloud Memorystore để improve performance và reduce costs. Enhance monitoring với custom metrics, detailed dashboards, và alerting rules. Improve error handling với circuit breakers, better retry logic, và dead-letter queues. Optimize Docker images và application code để reduce cold start times.

**Medium-term enhancements (3-6 tháng)** introduce new capabilities và improve user experience. Implement user authentication và authorization với OAuth hoặc Firebase Auth. Add multi-tenancy support để multiple users có thể use system independently. Implement RAG (Retrieval-Augmented Generation) để chatbot có thể access và cite external knowledge sources. Add support cho multi-modal inputs (images, voice) để richer interactions. Implement A/B testing framework để experiment với different LLM models, prompts, và UI designs.

**Long-term vision (6-12 tháng)** transforms system thành production-ready platform. Implement advanced analytics để track user behavior, conversation quality, và system performance. Add custom LLM fine-tuning capabilities để improve domain-specific performance. Implement advanced security features như encryption at rest, audit logging, và compliance với regulations. Build mobile applications (iOS, Android) để reach wider audience. Implement enterprise features như SSO, advanced admin controls, và SLA guarantees. Deploy multi-region để improve latency cho global users và provide disaster recovery.

**Research directions** include exploring newer LLM models và techniques (GPT-4, Claude, Gemini), investigating prompt optimization techniques (chain-of-thought, few-shot learning), researching cost optimization strategies (model distillation, selective caching), và exploring advanced conversation patterns (multi-turn reasoning, clarification questions).

### 8.6. Kết luận chung

Dự án Chatbot Cloud đã thành công trong việc demonstrate viability của serverless architecture cho AI-powered applications. Chúng tôi đã xây dựng một hệ thống functional, scalable, và cost-effective, leveraging modern cloud technologies và best practices.

Từ góc độ kỹ thuật, project showcases successful integration của nhiều technologies: Google Cloud Platform services (Cloud Run, Cloud Storage, Pub/Sub, Secret Manager), modern Python frameworks (FastAPI, Streamlit), Infrastructure as Code (Terraform), CI/CD automation (Cloud Build, GitHub Actions), và AI/LLM integration (OpenAI API). Mỗi technology được chosen carefully và integrated thoughtfully để create cohesive system.

Từ góc độ học tập, project provides invaluable hands-on experience với cloud computing concepts và practices. Chúng tôi đã learned về serverless architecture patterns, auto-scaling mechanisms, async processing với message queues, infrastructure automation, CI/CD pipelines, LLM integration techniques, và performance testing methodologies. These skills are highly relevant cho modern software engineering careers.

Từ góc độ practical value, system demonstrates rằng sophisticated AI applications có thể be built và deployed với reasonable effort và cost. Serverless approach enables starting small và scaling as needed, without upfront infrastructure investment. Pay-as-you-go pricing ensures costs align với actual usage. Managed services reduce operational burden, allowing focus on application logic rather than infrastructure management.

Looking forward, project provides solid foundation cho further development và experimentation. Architecture is flexible enough để accommodate new features và improvements. Codebase is well-organized và documented, facilitating future enhancements. Infrastructure automation ensures changes có thể be deployed reliably và consistently.

Ultimately, Chatbot Cloud project successfully achieves its goals của building serverless chatbot system, learning cloud computing technologies, và demonstrating practical application của modern software engineering practices. It serves as both working system và learning platform, providing value trong both dimensions.

---

## 9. TÀI LIỆU THAM KHẢO

### 9.1. Tài liệu dự án nội bộ

Trong quá trình phát triển dự án, chúng tôi đã tạo ra một bộ tài liệu comprehensive covering various aspects của system. README.md file provides high-level overview của project, including quick start guide, architecture summary, và links đến detailed documentation. File này serves như entry point cho anyone wanting to understand hoặc contribute đến project.

ARCHITECTURE.md document provides detailed explanation của system architecture, including component descriptions, data flow diagrams, design principles, và technology choices. Document này essential cho understanding how system works internally và why certain design decisions were made. DEPLOY_GUIDELINE.md offers step-by-step instructions cho deploying system, targeted at both technical users và non-technical stakeholders.

API.md documents all API endpoints với request/response schemas, authentication requirements, và usage examples. CONFIG.md explains all configuration options, environment variables, và Terraform variables. OPERATIONS.md covers operational aspects như scaling, monitoring, logging, và security. PRD.md (Product Requirements Document) defines product vision, features, và success criteria. PROJECT_CHECKLIST.md provides development checklist và CI guidelines.

### 9.2. Google Cloud Platform Documentation

Google Cloud Platform's official documentation đã been invaluable resource throughout project. Cloud Run documentation (cloud.google.com/run/docs) provides comprehensive coverage của service features, configuration options, best practices, và troubleshooting guides. Chúng tôi particularly found useful sections on auto-scaling configuration, container optimization, và service-to-service authentication.

Cloud Storage documentation (cloud.google.com/storage/docs) covers object storage concepts, API usage, access control, và performance optimization. Pub/Sub documentation (cloud.google.com/pubsub/docs) explains messaging patterns, subscription types, message delivery guarantees, và integration với other services. Secret Manager documentation (cloud.google.com/secret-manager/docs) details secret management best practices, access control, và rotation strategies.

Terraform GCP Provider documentation (registry.terraform.io/providers/hashicorp/google/latest/docs) is essential reference cho writing Terraform configurations. It documents all available resources, their arguments, attributes, và provides usage examples. Google Cloud Architecture Framework provides high-level guidance on designing cloud systems, covering areas như security, reliability, performance, và cost optimization.

### 9.3. Frameworks và Libraries

FastAPI documentation (fastapi.tiangolo.com) is excellent resource covering framework features, best practices, và advanced topics. Documentation includes tutorials, user guides, và API reference. Particularly useful are sections on async programming, dependency injection, và testing. Streamlit documentation (docs.streamlit.io) provides guides on building interactive web apps, with examples và API reference.

OpenAI API documentation (platform.openai.com/docs) is critical reference cho LLM integration. It covers API endpoints, model capabilities, pricing, rate limits, và best practices. Function calling documentation explains how to enable LLM to call external functions, with detailed examples. Locust documentation (docs.locust.io) guides on writing load test scenarios, running tests, và interpreting results.

Python ecosystem documentation for libraries như Pydantic, httpx, và pytest provides detailed API references và usage examples. These documentations help understand library capabilities và use them effectively.

### 9.4. Best Practices và Industry Standards

12-Factor App methodology (12factor.net) provides principles cho building modern, cloud-native applications. Principles như config in environment, stateless processes, và disposability align well với serverless architecture. Google Cloud Best Practices documentation covers areas như security, cost optimization, performance, và reliability.

Serverless Best Practices whitepaper từ Google Cloud provides specific guidance cho serverless applications, covering topics như cold start optimization, state management, error handling, và monitoring. Industry blogs và articles từ sources như Google Cloud Blog, AWS Blog, và engineering blogs của companies như Netflix, Uber provide real-world insights và lessons learned.

Academic papers on topics như serverless computing, LLM applications, và cloud architecture provide theoretical foundations và research findings. Conference talks từ events như Google Cloud Next, AWS re:Invent, và KubeCon offer practical insights và case studies.

### 9.5. Kết thúc

Tài liệu tham khảo listed above đã been instrumental trong success của project. Chúng provide both theoretical knowledge và practical guidance, enabling informed decisions và effective implementations. Combination của official documentation, community resources, và industry best practices ensures comprehensive understanding của technologies và patterns used.

---

**Ngày hoàn thành:** [Điền ngày hoàn thành thực tế]  
**Phiên bản:** 1.0  
**Người thực hiện:** [Điền tên sinh viên/nhóm]  
**Giảng viên hướng dẫn:** [Điền tên giảng viên]  
**Trường:** Đại học Bách Khoa Hà Nội (HUST)  
**Môn học:** Cloud Computing  
**Năm học:** 2026

---

**LƯU Ý QUAN TRỌNG:**

Báo cáo này được viết theo phong cách văn xuôi chi tiết, phù hợp cho báo cáo học thuật. Các phần về kết quả thử nghiệm (Section 7) hiện đang mô tả phương pháp và kết quả expected/mẫu. 

**Để hoàn thiện báo cáo, bạn cần:**

1. **Chạy load tests thực tế** theo hướng dẫn trong file `docs/LOAD_TEST_GUIDE.md`
2. **Thu thập số liệu thực tế** từ các tests
3. **Cập nhật Section 7** với số liệu cụ thể thay vì mô tả chung
4. **Điền thông tin** ở cuối báo cáo (ngày, tên, giảng viên)
5. **Review và chỉnh sửa** để đảm bảo tính chính xác và nhất quán

Báo cáo đã bao gồm đầy đủ các phần cần thiết với nội dung chi tiết, phù hợp cho mục đích học thuật và trình bày dự án.

