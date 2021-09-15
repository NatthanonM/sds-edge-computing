<template>
  <div class="main">
    <h1>Welcome</h1>
    <table>
      <tr>
        <th>Query ID</th>
        <th>Response (Architecture A)</th>
        <th>Response (Architecture B)</th>
        <th>Query by Using</th>
      </tr>
      <tr v-for="(query, index) in queries" :key="query.qId">
        <td>{{ query.qId }}</td>
        <td class="response">
          <div>
            <span class="title">Location: </span
            >{{
              query.responseA ? JSON.stringify(query.responseA.location) : ""
            }}
          </div>
          <div>
            <span class="title">Response time: </span>
            {{ query.responseA ? `${query.responseA.responseTime} ms` : "" }}
          </div>
        </td>
        <td class="response">
          <div>
            <span class="title">Location: </span
            >{{
              query.responseB ? JSON.stringify(query.responseB.location) : ""
            }}
          </div>
          <div>
            <span class="title">Response time: </span>
            {{ query.responseB ? `${query.responseB.responseTime} ms` : "" }}
          </div>
        </td>
        <td>
          <div class="mode-selector">
            <button @click="queryArch('A', query.qId, index)">
              Architecture A
            </button>
            <button @click="queryArch('B', query.qId, index)">
              Architecture B
            </button>
          </div>
        </td>
      </tr>
    </table>
  </div>
</template>

<script>
import queryService from "../service/api";
export default {
  name: "Home",
  data() {
    return {
      // EditHere
      queries: [
        {
          qId: "1",
          responseA: null,
          responseB: null,
        },
        {
          qId: "2",
          responseA: null,
          responseB: null,
        },
        {
          qId: "3",
          responseA: null,
          responseB: null,
        },
        {
          qId: "4",
          responseA: null,
          responseB: null,
        },
        {
          qId: "5",
          responseA: null,
          responseB: null,
        },
      ],
    };
  },
  methods: {
    async queryArch(arch, qId, index) {
      await queryService
        .indoorQuery(arch, qId)
        .then((response) => {
          // console.log(response);
          if (arch === "A") this.queries[index].responseA = response;
          if (arch === "B") this.queries[index].responseB = response;
        })
        .catch((err) => {
          console.log(err.message);
        });
    },
  },
};
</script>
<style scoped>
.main {
  padding: 10px 20px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.mode-selector {
  display: flex;
  column-gap: 30px;
  justify-content: center;
}
table {
  font-family: arial, sans-serif;
  border-collapse: collapse;
  width: 100%;
  margin: 20px 0;
}

td,
th {
  border: 1px solid #dddddd;
  text-align: left;
  padding: 8px;
  text-align: center;
}

tr:nth-child(even) {
  background-color: #f4f2f2;
}

button {
  min-height: 30px;
}
.title {
  color: #6e5aa5;
  font-weight: bolder;
  margin-right: 10px;
}
.response {
  text-align: left;
}
</style>
