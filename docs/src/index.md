---
title: Lance
hide:
  - navigation
  - toc
---

<div class="lance-home">
  <section class="mdx-container">
    <div class="container">
      <div class="intro-message">
        <div class="hero-logo">
          <img src="logo/white.png" alt="Lance logo" />
          <h1>Lance<sup>TM</sup></h1>
        </div>
        <h3>The Open Lakehouse Format for Multimodal AI</h3>
        <hr class="intro-divider" />
        <ul class="list-inline">
          <li><a href="quickstart/" class="lance-btn lance-btn--primary">Get Started</a></li>
          <li><a href="format/" class="lance-btn">Read the Spec</a></li>
          <li><a href="examples/python/llm_training/" class="lance-btn">Train an LLM</a></li>
          <li><a href="https://discord.gg/lance" class="lance-btn" target="_blank" rel="noopener">Join Discord</a></li>
        </ul>
      </div>
    </div>
  </section>

  <section class="lance-intro-section">
    <div class="container">
      <div class="lance-intro-content">
        <h2>What is Lance?</h2>
        <p>
          Lance is a modern, open source lakehouse format for multimodal AI. It contains a file format,
          table format, and catalog spec, allowing you to build a complete open lakehouse on top of object
          storage to power your AI workflows. Lance brings high-performance vector search, full-text search,
          random access, and feature engineering capabilities to the lakehouse, while you can still get all
          the existing lakehouse benefits like SQL analytics, ACID transactions, time travel, and integrations
          with open engines (Apache Spark, Ray, PyTorch, Trino, DuckDB, etc.) and open catalogs (Apache Polaris,
          Unity Catalog, Apache Gravitino, Hive Metastore, etc.).
        </p>
        <p>
          Learn more about Lance's technical details by reading our
          <a href="https://arxiv.org/abs/2504.15247" class="lance-paper-link" target="_blank" rel="noopener">research paper</a>
          published at <em>VLDB 2025</em>.
        </p>
        <a href="quickstart/" class="lance-btn lance-btn--primary">Read the Docs</a>
      </div>
    </div>
  </section>

  <section class="lance-feature-section">
    <div class="container">
      <div class="lance-feature-content">
        <div class="lance-feature-text">
          <h2>Expressive Hybrid Search</h2>
          <p>
            Lance enables powerful hybrid search combining vector similarity, full-text search,
            and SQL analytics on the same dataset. All query types are accelerated by corresponding
            secondary indexes as part of the Lance specification.
          </p>
          <p>
            Run semantic search on embeddings, BM25 search on keywords, and apply complex SQL predicates
            all using a single table with a unified interface.
          </p>
          <a href="quickstart/vector-search/" class="lance-link-btn">Learn More</a>
        </div>
        <div class="lance-feature-demo">
          <img src="assets/images/hybrid-search.png" alt="Hybrid search example" />
        </div>
      </div>
    </div>
  </section>

  <section class="lance-feature-section reverse">
    <div class="container">
      <div class="lance-feature-content">
        <div class="lance-feature-text">
          <h2>Lightning-fast Random Access</h2>
          <p>
            Lance delivers 100x faster random access compared to Parquet or Iceberg. Unlike traditional
            formats, Lance maintains high performance even when randomly accessing scattered rows across
            your entire dataset.
          </p>
          <p>
            With a highly optimized file format plus efficient row-addressing and secondary indexes at table level,
            you can access individual records across multiple files instantly, making it perfect for real-time ML serving,
            random sampling, and interactive applications.
          </p>
          <a href="guide/read_and_write/#random-access" class="lance-link-btn">Learn More</a>
        </div>
        <div class="lance-feature-demo">
          <img src="assets/images/random-access.png" alt="Random access example" />
        </div>
      </div>
    </div>
  </section>

  <section class="lance-feature-section">
    <div class="container">
      <div class="lance-feature-content">
        <div class="lance-feature-text">
          <h2>Native Multimodal Data Support</h2>
          <p>
            Store images, videos, audio, text, and embeddings alongside your traditional tabular data in a single
            unified format. Lance's blob encoding efficiently handles large binary objects with lazy loading, while
            optimized vector storage accelerates similarity search.
          </p>
          <p>
            Perfect for AI and ML workloads where you need to store raw data, ML features, generated captions and
            embeddings all together for multimodal retrieval and genAI workflows.
          </p>
          <a href="guide/blob/" class="lance-link-btn">Learn More</a>
        </div>
        <div class="lance-feature-demo">
          <img src="assets/images/multimodal-data.png" alt="Multimodal data example" />
        </div>
      </div>
    </div>
  </section>

  <section class="lance-feature-section reverse">
    <div class="container">
      <div class="lance-feature-content">
        <div class="lance-feature-text">
          <h2>Data Evolution > Schema Evolution</h2>
          <p>
            Schema evolution in most open table formats are metadata only and fast. But when trying to backfill
            column values in existing rows, a full table rewrite is typically required. Lance supports data evolution
            (efficient schema evolution with backfill), making it ideal for ML feature engineering, embedding and
            media content management.
          </p>
          <p>
            Adding a new column with data is as simple as writing new Lance files to the Lance table, with no need
            to rewrite your entire dataset.
          </p>
          <a href="guide/data_evolution/" class="lance-link-btn">Learn More</a>
        </div>
        <div class="lance-feature-demo">
          <img src="assets/images/data-evolution.png" alt="Data evolution example" />
        </div>
      </div>
    </div>
  </section>

  <section class="lance-feature-section">
    <div class="container">
      <div class="lance-feature-content">
        <div class="lance-feature-text">
          <h2>Rich Ecosystem Integrations</h2>
          <p>
            As an open format, Lance integrates seamlessly with the Python data ecosystem and modern data platforms.
            Work with your favorite tools including Pandas, Polars, Ray and PyTorch for data processing and machine learning.
          </p>
          <p>
            Connect with leading query engines like Apache DataFusion, DuckDB, Apache Spark, Trino, and Apache Flink/Fluss
            to run SQL analytics and distributed processing on your Lance datasets.
          </p>
          <a href="integrations/datafusion/" class="lance-link-btn">View Integrations</a>
        </div>
        <div class="lance-feature-demo">
          <img src="assets/images/ecosystem-integrations.png" alt="Lance ecosystem integrations" />
        </div>
      </div>
    </div>
  </section>
</div>
