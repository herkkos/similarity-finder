using Backend.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Http;
using System.Web.Http.Description;
using System.Web.Mvc;

namespace Backend.Controllers
{
    public class UserController : ApiController
    {
        private User[] users = new User[]
        {
            new User { id = 1, name = "Karem", email = "email1@mail.com", phone = "011111", role = 1 },
            new User { id = 2, name = "Jorem", email = "email2@mail.com", phone = "001111", role = 0 }
        };

        // GET: User
        [ResponseType(typeof(IEnumerable<User>))]
        public IEnumerable<User> Get()
        {
            return users;
        }

        // GET: api/Users/5
        public IHttpActionResult Get(int id)
        {
            var product = users.FirstOrDefault((p) => p.id == id);
            if (product == null)
            {
                return NotFound();
            }
            return Ok(product);
        }

    }
}
