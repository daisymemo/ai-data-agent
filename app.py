from src.text2sql import ask
import streamlit as st


st.set_page_config(
    page_title="AI Data Agent",
    page_icon="📊",
    layout="wide"
)


st.title("📊 AI Data Agent")
st.caption("基于 RAG + Text2SQL 的智能数据查询助手")


question = st.text_input(
    "请输入你的数据问题",
    placeholder="例如：不同营销渠道的转化率是多少？"
)


if st.button("开始分析"):

    if not question:
        st.warning("请先输入一个问题")

    else:
        with st.spinner("正在分析数据..."):

            try:
                response = ask(question)

                st.subheader("AI 分析")
                st.write(response["answer"])

                st.subheader("查询结果")
                st.dataframe(
                    response["result"],
                    use_container_width=True
                )
                st.subheader("SQL 安全校验")
                st.success(f"✅ {response['validation_message']}")
                with st.expander("查看 RAG 检索依据"):
                    for i, chunk in enumerate(response["retrieved_chunks"], start=1):
                        st.markdown(f"**Top {i} · {chunk['source']}**")
                        st.caption(f"相关度：{chunk['score']:.4f}")
                        st.code(chunk["content"], language="text")
                with st.expander("查看生成的 SQL"):
                    st.code(
                        response["sql"],
                        language="sql"
                    )

            except Exception as e:
                st.error(f"分析失败：{e}")