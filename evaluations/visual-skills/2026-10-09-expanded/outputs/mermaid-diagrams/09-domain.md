```mermaid
classDiagram
    class Order[订单]
    class Item[订单项] {
        下单单价快照
    }
    class Product[商品] {
        当前价格
    }
    Order "1" -- "1..*" Item : 包含
    Item "0..*" --> "1" Product : 引用
    note for Item "商品当前价格变化，不得改写下单单价快照"
```

每个订单至少有一个订单项，每项只属于一个订单；每项引用一个商品，商品可以被零个或多个订单项引用。历史单价以订单项快照为准。图表达领域规则，表结构、外键、级联删除与ORM映射尚未设计。
